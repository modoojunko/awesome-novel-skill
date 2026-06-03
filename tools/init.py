#!/usr/bin/env python3
"""
awesome-novel-skill 项目初始化工具

用法: python init.py <project-path>

从 skill 仓库复制 agent 定义、题材知识、记忆规则到用户项目目录，
创建完整的小说写作项目骨架。
"""

import sys
import os
import shutil
from pathlib import Path


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
SOURCE_MEMORY = SKILL_HOME / "memory"
SOURCE_ANTI_AI = SKILL_HOME / "memory" / "anti-ai"
SOURCE_WRITER_STYLE = SKILL_HOME / "memory" / "writer-style"  # optional
SOURCE_GENRE_EXAMPLE = SKILL_HOME / "knowledge" / "genre-example"
SOURCE_FORMAT_SPECS = SKILL_HOME / "knowledge" / "format-specs"


def main():
    if len(sys.argv) < 2:
        print("用法: python init.py <project-path>")
        sys.exit(1)

    project_path = Path(sys.argv[1]).resolve()

    if project_path.exists():
        print(f"错误: {project_path} 已存在")
        sys.exit(1)

    print(f"初始化小说项目: {project_path}")
    print(f"技能仓库: {SKILL_HOME}")

    # Step 1: 选题材
    genre = select_genre()

    # Step 2: 创建骨架
    create_skeleton(project_path)

    # Step 3: 部署 agent 定义
    deploy_agents(project_path)

    # Step 4: 按题材继承记忆
    deploy_memory(project_path, genre)

    # Step 5: 按题材继承知识
    deploy_knowledge(project_path, genre)

    # Step 6: 生成 CLAUDE.md
    write_claude_md(project_path)

    # Step 7: 生成 MEMORY.md 索引
    write_memory_index(project_path)

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
        "archives",
        ".agent/task",
        ".claude/agents",
        ".claude/memory",
        ".claude/knowledge",
    ]
    for d in dirs:
        (project_path / d).mkdir(parents=True)

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

    print(f"  ✅ 已继承 {count} 个知识文件")


def write_claude_md(project_path: Path):
    """生成项目根目录的 CLAUDE.md"""
    claude_md = """# {project_name}

## AI 指引

本项目的写作流程由 7 个 agent 协作完成，定义在 `.claude/agents/` 下。

**开始写作：** 输入 `@novel-agent` 进入写作循环。

**项目结构：**
- `story.md` — 项目索引 + 主线拆纲
- `settings/` — 世界观、角色、写作风格、时间线
- `volumes/` — 卷纲
- `chapters/` — 章纲
- `prompts/` — 提示词
- `archives/` — 正文
- `.agent/` — 状态追踪 + agent 通信
- `.claude/knowledge/` — 反 AI 规则、文风偏好、题材参考材料
"""
    (project_path / "CLAUDE.md").write_text(
        claude_md.format(project_name=project_path.name), encoding="utf-8"
    )


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


if __name__ == "__main__":
    main()
