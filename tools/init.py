#!/usr/bin/env python3
"""
awesome-novel-skill 项目初始化工具

用法: python init.py [project-path] [--genre <编号>]

从 skill 仓库复制 agent 定义、题材知识、记忆规则到用户项目目录，
创建完整的小说写作项目骨架。

不带参数时默认在当前目录初始化。
"""

import sys
import os
import shutil
from pathlib import Path

# 强制 UTF-8 编码，避免 Windows 终端中文乱码
for s in (sys.stdin, sys.stdout, sys.stderr):
    try:
        s.reconfigure(encoding="utf-8")
    except AttributeError:
        pass


GENRES = [
    "xianxia", "xuanhuan", "urban", "urban-romance", "urban-daily",
    "urban-farming", "urban-brained", "western-fantasy", "ancient-politics",
    "historical", "anti-japanese-war", "scifi-apocalypse", "war-god",
    "suspense-crime", "suspense-paranormal", "anime-derivative",
    "derivative", "fanqie",
]

SKILL_HOME = Path(os.environ.get("NOVEL_SKILL_HOME", Path(__file__).parent.parent))

SOURCE_AGENTS = SKILL_HOME / "agents"
SOURCE_KNOWLEDGE = SKILL_HOME / "knowledge"
SOURCE_TEMPLATES = SKILL_HOME / "templates"
SOURCE_MEMORY = SKILL_HOME / "memory"  # no-op since anti-ai/writer-style moved to knowledge/
SOURCE_ANTI_AI = SKILL_HOME / "knowledge" / "anti-ai"
SOURCE_WRITER_STYLE = SKILL_HOME / "memory" / "writer-style"  # optional
SOURCE_GENRE_EXAMPLE = SKILL_HOME / "knowledge" / "genre-example"
SOURCE_FORMAT_SPECS = SKILL_HOME / "knowledge" / "format-specs"


def main():
    if "-h" in sys.argv or "--help" in sys.argv:
        print(__doc__.strip())
        return

    if len(sys.argv) >= 2 and not sys.argv[1].startswith("--"):
        project_path = Path(sys.argv[1]).resolve()
    else:
        project_path = Path.cwd()

    # 解析可选参数
    genre = None
    if "--genre" in sys.argv:
        idx = sys.argv.index("--genre")
        if idx + 1 < len(sys.argv):
            try:
                genre = GENRES[int(sys.argv[idx + 1]) - 1]
            except (IndexError, ValueError):
                print(f"无效题材编号，可选 1-{len(GENRES)}")
                sys.exit(1)

    if project_path.exists():
        print(f"目录已存在，将在其中创建缺失的文件和目录")
    else:
        project_path.mkdir(parents=True)

    print(f"初始化小说项目: {project_path}")
    print(f"技能仓库: {SKILL_HOME}")

    # Step 1: 选题材
    if genre is None:
        genre = select_genre()
    else:
        print(f"题材: {genre}")

    # Step 2: 创建骨架
    create_skeleton(project_path)

    # Step 3: 部署 agent 定义
    deploy_agents(project_path)

    # Step 4: 按题材继承记忆
    deploy_memory(project_path, genre)

    # Step 5: 按题材继承知识
    deploy_knowledge(project_path, genre)

    # Step 6: 生成 MEMORY.md 索引
    write_memory_index(project_path)

    # Step 7: 初始化写作记忆文件
    init_memory_files(project_path)

    # Step 8: 初始化状态
    write_status(project_path)

    print(f"\n初始化完成!")
    print(f"项目路径: {project_path}")
    print(f"输入 @novel-agent 开始写作")


def select_genre() -> str:
    """交互式选题材"""
    print("\n可选题材:")
    for i, g in enumerate(GENRES, 1):
        print(f"  {i:2d}. {g}")

    while True:
        try:
            choice = input("\n选择题材编号: ").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(GENRES):
                return GENRES[idx]
        except ValueError:
            pass
        print("无效选择，请重试")


def create_skeleton(project_path: Path):
    """创建项目目录结构"""
    dirs = [
        "settings/character-setting",
        "volumes",
        "chapters",
        "prompts",
        "sandbox",
        "archives",
        ".agent/task",
        ".claude/agents",
        ".claude/memory",
        ".claude/knowledge",
    ]
    for d in dirs:
        (project_path / d).mkdir(parents=True, exist_ok=True)

    # Copy template files into project (skip migration/ — old project upgrade only)
    if SOURCE_TEMPLATES.exists():
        for item in SOURCE_TEMPLATES.rglob("*"):
            if item.is_file() and item.name != ".gitkeep":
                rel_path = item.relative_to(SOURCE_TEMPLATES)
                if rel_path.parts[0] == "migration":
                    continue
                target = project_path / rel_path
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, target)
        print("  ✅ 已拷贝项目模板")


def deploy_agents(project_path: Path):
    """复制所有 agent 定义和 agent skill 到项目 .claude/agents/"""
    target = project_path / ".claude" / "agents"
    if SOURCE_AGENTS.exists():
        count = 0
        for item in SOURCE_AGENTS.rglob("*"):
            if item.is_file() and item.suffix == ".md":
                rel_path = item.relative_to(SOURCE_AGENTS)
                dest = target / rel_path
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, dest)
                count += 1
        print(f"  ✅ 已部署 {count} 个 agent/skill 文件")
    else:
        print("  ⚠️  agent 目录不存在，跳过")


def deploy_memory(project_path: Path, genre: str):
    """初始化 memory 目录（占位，反 AI/文风已移至 knowledge）"""
    pass


def deploy_knowledge(project_path: Path, genre: str):
    """按题材拷贝参考材料 + 反 AI/文风规则到 .claude/knowledge/"""
    knowledge_dir = project_path / ".claude" / "knowledge"
    count = 0

    # 从 knowledge/format-specs/ 复制格式规范
    if SOURCE_FORMAT_SPECS.exists():
        for f in SOURCE_FORMAT_SPECS.glob("*.md"):
            shutil.copy2(f, knowledge_dir / f.name)
            count += 1

    # 题材案例
    genre_example_src = SOURCE_GENRE_EXAMPLE / f"{genre}.md"
    if genre_example_src.exists():
        shutil.copy2(genre_example_src, knowledge_dir / "genre-example.md")
        count += 1

    # 反 AI 规则：通用 + 题材
    anti_ai_content = []
    anti_ai_content.append("# 反 AI 规则\n\n[community-defaults]\n")
    common_rules = SOURCE_ANTI_AI / "common-rules.md"
    if common_rules.exists():
        anti_ai_content.append(common_rules.read_text(encoding="utf-8"))

    genre_rules = SOURCE_ANTI_AI / f"{genre}.md"
    if genre_rules.exists():
        anti_ai_content.append(f"\n[community-defaults] 题材: {genre}\n")
        anti_ai_content.append(genre_rules.read_text(encoding="utf-8"))

    if anti_ai_content:
        (knowledge_dir / "anti-ai.md").write_text(
            "\n".join(anti_ai_content), encoding="utf-8"
        )
        count += 1
        print(f"  ✅ 已继承反 AI 规则 (通用 + {genre})")

    # 文风偏好
    style_dir = SOURCE_WRITER_STYLE / genre
    if style_dir.exists():
        style_content = []
        for sf in style_dir.glob("*.md"):
            style_content.append(sf.read_text(encoding="utf-8"))
        if style_content:
            (knowledge_dir / "writer-style.md").write_text(
                f"# 文风偏好\n\n[community-defaults] 题材: {genre}\n\n"
                + "\n".join(style_content),
                encoding="utf-8",
            )
            count += 1
            print(f"  ✅ 已继承文风偏好 ({genre})")

    # 永久记忆占位文件（空，后续由 updater 晋升填充）
    permanent_memory = knowledge_dir / "permanent-memory.md"
    if not permanent_memory.exists():
        permanent_memory.write_text(
            "# 永久记忆\n\n> 从 .claude/memory/ 晋升的高频条目，"
            "内容格式与 memory 条目一致，由 updater 在兜底 sweep 时维护。\n\n"
            "---\n\n## 条目列表\n",
            encoding="utf-8",
        )
        count += 1

    # 创作方法论目录（plot-craft / scene-craft / character-craft / title-craft）
    craft_dirs = ["plot-craft", "scene-craft", "character-craft", "title-craft"]
    for dir_name in craft_dirs:
        src = SOURCE_KNOWLEDGE / dir_name
        if src.exists() and src.is_dir():
            dst = knowledge_dir / dir_name
            shutil.copytree(src, dst, dirs_exist_ok=True)
            file_count = sum(1 for _ in src.rglob("*") if _.is_file())
            count += file_count
            print(f"  ✅ 已部署 {dir_name}/ ({file_count} 个文件)")

    print(f"  ✅ 已继承 {count} 个知识文件")


def write_status(project_path: Path):
    """初始化 .agent/status.md"""
    status = """# 项目状态

- **skill_version:** 4.0
- **phase:** setup
- **current_volume:**
- **current_chapter:**
- **last_archived:**
- **next_task:** 填写基础设定（世界观/角色/写作风格）
"""
    (project_path / ".agent" / "status.md").write_text(status, encoding="utf-8")


def write_memory_index(project_path: Path):
    """生成 .claude/memory/MEMORY.md 占位索引"""
    memory_dir = project_path / ".claude" / "memory"
    (memory_dir / "MEMORY.md").write_text("# 写作记忆库\n\n（暂无记忆）\n", encoding="utf-8")


MEMORY_FILES = {
    "volume-memory.md": (
        "# 卷纲写作记忆\n\n> 记录卷纲规划环节中作者的反馈"
        "（冲突设计、节奏分布、章节结构等）。\n\n**相关 Agent:** volume-planner\n"
        "**相关 Skill:** volume-arc, volume-direction, volume-writing\n\n"
        "---\n\n## 条目列表\n"
    ),
    "chapter-memory.md": (
        "# 章纲写作记忆\n\n> 记录章纲规划环节中作者的反馈"
        "（场景设计、情绪节奏、伏笔安排等）。\n\n**相关 Agent:** chapter-planner\n"
        "**相关 Skill:** chapter-reference, chapter-outline, chapter-verify\n\n"
        "---\n\n## 条目列表\n"
    ),
    "prompt-memory.md": (
        "# 提示词写作记忆\n\n> 记录提示词组装环节中作者的反馈"
        "（层结构、注入规则、指令清晰度等）。\n\n**相关 Agent:** prompt-crafter\n"
        "**相关 Skill:** prompt-crafting\n\n"
        "---\n\n## 条目列表\n"
    ),
    "writing-memory.md": (
        "# 正文写作记忆\n\n> 记录正文写作和读者验收环节中作者的反馈"
        "（文风、爽点、节奏、描写等）。\n\n**相关 Agent:** writer, reader\n"
        "**相关 Skill:** writing-execution, reader-review\n\n"
        "---\n\n## 条目列表\n"
    ),
}


def init_memory_files(project_path: Path):
    """初始化 4 个写作记忆文件"""
    memory_dir = project_path / ".claude" / "memory"
    for filename, content in MEMORY_FILES.items():
        filepath = memory_dir / filename
        if not filepath.exists():
            filepath.write_text(content, encoding="utf-8")
    print("  \u2705 \u5df2\u521d\u59cb\u5316 4 \u4e2a\u5199\u4f5c\u8bb0\u5fc6\u6587\u4ef6")





if __name__ == "__main__":
    main()
