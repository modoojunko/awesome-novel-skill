#!/usr/bin/env python3
# awesome-novel-skill - AI-assisted novel writing workflow system
# Copyright (C) 2026  modoojunko
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
Novel Agent Skill - 已有小说导入脚本

用法:
    python import.py <项目路径> <小说文件> [--format txt|md]
"""

import argparse
import re
import os
from pathlib import Path


CHAPTER_PATTERNS = [
    # 中文: 第X章 / 第X卷 第Y章
    re.compile(r'^第[一二三四五六七八九十百千\d]+章\s*[^\n]*$', re.MULTILINE),
    re.compile(r'^第[一二三四五六七八九十百千\d]+卷\s*第[一二三四五六七八九十百千\d]+章\s*[^\n]*$', re.MULTILINE),
    # 中文: 章X / Chapter X / CH X
    re.compile(r'^[Cc]hapter\s*\d+[^\n]*$', re.MULTILINE),
    re.compile(r'^[Cc][Hh]\s*\d+[^\n]*$', re.MULTILINE),
    # 分隔线形式的章节标记
    re.compile(r'^#+\s*(第[一二三四五六七八九十百千\d]+章|Chapter\s*\d+)', re.MULTILINE),
]


def detect_chapter_pattern(text: str) -> tuple[re.Pattern, list[re.Match]] | None:
    """检测文本使用的章节标记模式，返回(匹配模式, 匹配列表)"""
    for pattern in CHAPTER_PATTERNS:
        matches = list(pattern.finditer(text))
        if len(matches) >= 2:  # 至少找到2个匹配才认为有效
            return pattern, matches
    return None


def split_chapters(text: str) -> list[tuple[str, str]]:
    """
    将文本按章节切分。

    Returns:
        list of (chapter_title, chapter_content) tuples
    """
    result = detect_chapter_pattern(text)
    if result is None:
        # 没有找到章节标记，整篇作为一章
        return [("第1章", text.strip())]

    pattern, matches = result
    chapters = []

    for i, match in enumerate(matches):
        title = match.group(0).strip()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        content = text[start:end].strip()
        chapters.append((title, content))

    return chapters


def slugify(title: str) -> str:
    """将章节标题转为可用于文件名的 slug"""
    # 提取中文或英文标题部分
    slug = title.strip()
    # 去掉 # 和多余空格
    slug = re.sub(r'^#+\s*', '', slug)
    # 限制长度
    if len(slug) > 50:
        slug = slug[:50]
    return slug


def write_chapter_archive(chapters_dir: Path, vol: int, ch: int,
                          title: str, content: str) -> Path:
    """将章节正文写入 archives/ 目录"""
    slug = slugify(title)
    filename = f"vol-{vol}-ch-{ch}-{slug}.md"
    filepath = chapters_dir / filename
    filepath.write_text(content, encoding='utf-8')
    return filepath


def write_chapter_outline(chapters_dir: Path, vol: int, ch: int,
                          title: str, word_count: int) -> Path:
    """为导入章节创建章纲 yaml（outline 字段留空等 Agent 填充）"""
    outline_path = chapters_dir / f"vol-{vol}-ch-{ch}.yaml"
    outline_path.write_text(f"""# vol-{vol}-ch-{ch}.yaml - 导入章节

volume: {vol}
chapter: {ch}
title: "{title}"

outline:
  summary: ""
  key_points: []
  characters: []
  location: ""
  time: ""

prompt_path: ""
status: "archived"
archive_path: "./archives/vol-{vol}-ch-{ch}-{slugify(title)}.md"
""", encoding='utf-8')
    return outline_path


def import_novel(project_path: str, novel_file: str) -> None:
    """
    导入已有小说文件到项目

    Args:
        project_path: 项目目录路径
        novel_file: 小说源文件路径
    """
    project = Path(project_path)
    novel = Path(novel_file)

    if not project.exists():
        print(f"错误：项目目录不存在: {project_path}")
        print("请先运行 init.py 创建项目")
        return

    if not novel.exists():
        print(f"错误：小说文件不存在: {novel_file}")
        return

    # 读取源文件
    text = novel.read_text(encoding='utf-8')
    print(f"已读取: {novel_file} ({len(text)} 字符)")

    # 切分章节
    chapters = split_chapters(text)
    print(f"检测到 {len(chapters)} 个章节")

    if len(chapters) == 1 and len(text) < 500:
        print("警告：未检测到章节标记，仅找到少量文本，请检查文件格式")

    # 确保目录存在
    archives_dir = project / "archives"
    chapters_yaml_dir = project / "chapters"
    archives_dir.mkdir(parents=True, exist_ok=True)
    chapters_yaml_dir.mkdir(parents=True, exist_ok=True)

    # 写入各章节
    for i, (title, content) in enumerate(chapters):
        vol = 1
        ch_num = i + 1
        word_count = len(content)

        archive_path = write_chapter_archive(archives_dir, vol, ch_num, title, content)
        outline_path = write_chapter_outline(chapters_yaml_dir, vol, ch_num, title, word_count)

        print(f"  第{ch_num}章: {title} ({word_count} 字) → {archive_path.name}")

    print(f"\n导入完成: {len(chapters)} 章已写入 archives/ 和 chapters/")
    print("下一步：请 Agent 逐章阅读正文，反向提取设定并填充 YAML 文件。")


def main():
    parser = argparse.ArgumentParser(description="导入已有小说文件")
    parser.add_argument("project_path", help="项目目录路径")
    parser.add_argument("novel_file", help="小说源文件 (.txt / .md)")
    args = parser.parse_args()

    import_novel(args.project_path, args.novel_file)


if __name__ == "__main__":
    main()
