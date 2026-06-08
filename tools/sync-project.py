#!/usr/bin/env python3
"""
同步项目空间的 agent/skill/知识库到最新版本。

用法:
  python tools/sync-project.py <project-path>            # 同步（自动更新指纹）
  python tools/sync-project.py <project-path> --check    # 只检查新鲜度
  python tools/sync-project.py <project-path> --sync     # 强制同步（同默认）

检查模式 (--check) 用 exit code 表示结果：
  0 = 已是最新
  1 = 有更新可用（或项目缺少指纹）
  2 = 项目无效

不触碰 settings/ volumes/ chapters/ archives/ prompts/ story.md。
"""

import hashlib
import sys
import os
import shutil
from pathlib import Path

for s in (sys.stdin, sys.stdout, sys.stderr):
    try:
        s.reconfigure(encoding="utf-8")
    except AttributeError:
        pass


SKILL_HOME = Path(__file__).parent.parent
AGENT_DIR = SKILL_HOME / "agents"
SKILL_DIR = SKILL_HOME / "skills"
KNOWLEDGE_DIR = SKILL_HOME / "knowledge"
FINGERPRINT_FILE = Path(".agent") / ".sync-fingerprint"


def main():
    if "-h" in sys.argv or "--help" in sys.argv or len(sys.argv) < 2:
        print(__doc__.strip())
        return

    check_only = "--check" in sys.argv

    project_path = Path(sys.argv[1]).resolve()
    if not project_path.exists():
        print(f"错误: 路径不存在: {project_path}")
        sys.exit(2)

    status_file = project_path / ".agent" / "status.md"
    if not status_file.exists():
        print(f"错误: {project_path} 不是有效的小说项目（缺少 .agent/status.md）")
        sys.exit(2)

    if check_only:
        check_freshness(project_path)
        return

    do_sync(project_path)


# ============================================================
# 指纹机制
# ============================================================

def compute_fingerprint() -> str:
    """对 skill 源目录的所有 agent/skill/knowledge 文件算一个 hash"""
    files = []
    for base in [AGENT_DIR, SKILL_DIR, KNOWLEDGE_DIR]:
        if base.exists():
            for f in sorted(base.rglob("*")):
                if f.is_file() and f.name != ".gitkeep":
                    files.append(f)

    h = hashlib.sha256()
    for f in files:
        rel = f.relative_to(SKILL_HOME)
        h.update(str(rel).encode("utf-8"))
        h.update(f.read_bytes())
    return h.hexdigest()


def read_project_fingerprint(project: Path) -> str | None:
    fp = project / FINGERPRINT_FILE
    if fp.exists():
        return fp.read_text(encoding="utf-8").strip()
    return None


def write_project_fingerprint(project: Path, fingerprint: str):
    fp = project / FINGERPRINT_FILE
    fp.parent.mkdir(parents=True, exist_ok=True)
    fp.write_text(fingerprint + "\n", encoding="utf-8")


# ============================================================
# 检查
# ============================================================

def check_freshness(project: Path):
    current = compute_fingerprint()
    stored = read_project_fingerprint(project)

    if stored is None:
        print("项目缺少同步指纹，无法判断新鲜度。运行 sync-project.py 同步后生成。")
        sys.exit(1)

    if current == stored:
        print("已是最新。")
        sys.exit(0)
    else:
        # 找出具体哪些文件变了
        changes = find_changes(project)
        print(f"有更新可用 ({len(changes)} 个文件发生变化):")
        for f in changes:
            print(f"  - {f}")
        sys.exit(1)


def find_changes(project: Path) -> list[str]:
    """返回与源不同的文件列表（相对路径）"""
    sources = {
        "agents": project / ".claude" / "agents",
        "skills": project / ".claude" / "skills",
        "knowledge": project / ".claude" / "knowledge",
    }
    changed = []

    for name, src_dir in [("agents", AGENT_DIR), ("skills", SKILL_DIR), ("knowledge", KNOWLEDGE_DIR)]:
        if not src_dir.exists():
            continue
        dst_dir = project / ".claude" / name
        for item in sorted(src_dir.rglob("*.md")):
            if item.name == ".gitkeep":
                continue
            rel = item.relative_to(src_dir)
            target = dst_dir / rel
            if not target.exists() or target.read_bytes() != item.read_bytes():
                changed.append(f"{name}/{rel}")

    return changed


# ============================================================
# 同步
# ============================================================

def do_sync(project: Path):
    print(f"项目: {project}")
    print(f"来源: {SKILL_HOME}")
    print()

    # 检查当前新鲜度
    current_fp = compute_fingerprint()
    stored_fp = read_project_fingerprint(project)
    if stored_fp == current_fp:
        print("[i] 已是最新，无需同步。")
        return

    changes = []
    changes.append(sync_agents(project))
    changes.append(sync_skills(project))
    changes.append(sync_knowledge(project))

    total = sum(c for c in changes if c > 0)

    if total > 0 or stored_fp != current_fp:
        write_project_fingerprint(project, current_fp)

    print(f"\n完成。共同步 {total} 个文件。")
    if total > 0:
        print("提示: 下次写作时生效。")


def sync_agents(project_path: Path) -> int:
    target = project_path / ".claude" / "agents"
    target.mkdir(parents=True, exist_ok=True)
    if not AGENT_DIR.exists():
        print("  [!] agents 源目录不存在，跳过")
        return 0
    count = _sync_dir(AGENT_DIR, target, "*.md")
    if count > 0:
        print(f"  [OK] agent 定义: {count} 个文件已更新")
    else:
        print(f"  [i] agent 定义: 已是最新")
    return count


def sync_skills(project_path: Path) -> int:
    target = project_path / ".claude" / "skills"
    target.mkdir(parents=True, exist_ok=True)
    if not SKILL_DIR.exists():
        print("  [!] skills 源目录不存在，跳过")
        return 0
    count = _sync_dir(SKILL_DIR, target, "*.md")
    if count > 0:
        print(f"  [OK] skill 文件: {count} 个文件已更新")
    else:
        print(f"  [i] skill 文件: 已是最新")
    return count


def sync_knowledge(project_path: Path) -> int:
    target = project_path / ".claude" / "knowledge"
    target.mkdir(parents=True, exist_ok=True)
    if not KNOWLEDGE_DIR.exists():
        print("  [!] knowledge 源目录不存在，跳过")
        return 0
    count = 0
    for f in KNOWLEDGE_DIR.glob("*.md"):
        if _sync_file(f, target / f.name):
            count += 1
    for subdir in KNOWLEDGE_DIR.iterdir():
        if subdir.is_dir() and not subdir.name.startswith("."):
            sub_target = target / subdir.name
            sub_target.mkdir(parents=True, exist_ok=True)
            count += _sync_dir(subdir, sub_target, "*.md")
    if count > 0:
        print(f"  [OK] 知识库: {count} 个文件已更新")
    else:
        print(f"  [i] 知识库: 已是最新")
    return count


def _sync_dir(src: Path, dst: Path, pattern: str) -> int:
    count = 0
    for item in sorted(src.rglob(pattern)):
        if item.name == ".gitkeep":
            continue
        rel = item.relative_to(src)
        target = dst / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if _sync_file(item, target):
            count += 1
    return count


def _sync_file(src: Path, dst: Path) -> bool:
    if dst.exists() and dst.read_bytes() == src.read_bytes():
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return True


if __name__ == "__main__":
    main()
