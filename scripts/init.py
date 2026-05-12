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
Novel Agent Skill - 项目初始化脚本

用法:
    python init.py [项目名]
"""

import argparse
import os
import shutil
import datetime
from pathlib import Path


def get_template_path(template_name: str) -> Path:
    """获取模板文件路径"""
    return Path(__file__).parent / "templates" / f"{template_name}.md.template"


def create_directory_structure(project_path: Path) -> None:
    """创建项目目录结构"""
    dirs = [
        project_path / "settings" / "character-setting",
        project_path / "volumes",
        project_path / "chapters",
        project_path / "prompts",
        project_path / "archives",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)


def copy_template(template_name: str, dest: Path) -> None:
    """复制模板文件到目标路径"""
    src = get_template_path(template_name)
    shutil.copy2(src, dest)


def copy_md_template(template_name: str, dest: Path) -> None:
    """复制 markdown 模板文件到目标路径"""
    src = Path(__file__).parent / "templates" / f"{template_name}.md.template"
    shutil.copy2(src, dest)


def init_project(project_name: str, author: str = "") -> None:
    """
    初始化小说项目

    Args:
        project_name: 项目名称
        author: 作者名
    """
    project_path = Path(project_name)

    # 创建目录结构
    create_directory_structure(project_path)

    # 复制模板文件
    copy_md_template("story", project_path / "story.md")
    copy_template("world-setting", project_path / "settings" / "world-setting.md")
    copy_template("writing-style", project_path / "settings" / "writing-style.md")
    copy_template("anti-ai", project_path / "settings" / "anti-ai.md")
    copy_template("hooks", project_path / "settings" / "hooks.md")

    # 复制角色设定模板（markdown 格式，角色文件后续讨论时创建）
    copy_md_template("character", project_path / "settings" / "character-setting" / "template.md")

    print(f"项目已创建: {project_path}")
    print(f"请进入项目目录: cd {project_path}")


def main():
    parser = argparse.ArgumentParser(description="初始化小说项目")
    parser.add_argument("project_name", help="项目名称")
    parser.add_argument("--author", default="", help="作者名")
    args = parser.parse_args()

    init_project(args.project_name, args.author)


if __name__ == "__main__":
    main()
