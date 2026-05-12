#!/usr/bin/env python3
"""
Novel Project Phase Detection — scan project files and determine current phase.

Outputs current_phase, current_volume, current_chapter to stdout as YAML-like key=value pairs.
Optionally updates .agent/status.md with --write.

Usage:
    python detect_phase.py [--write]
"""

import argparse
import datetime
import os
import re
import sys
from pathlib import Path

CHAPTER_STATUS_ORDER = {"outline": 0, "draft": 1, "archived": 2}


def read_status_cache(agent_dir: Path) -> dict:
    """Read .agent/status.md cache (basic YAML frontmatter parsing)."""
    status_file = agent_dir / "status.md"
    if not status_file.exists():
        return {}
    text = status_file.read_text(encoding="utf-8")
    result = {}
    for line in text.splitlines():
        m = re.match(r"^(\w+):\s*(.*)", line)
        if m:
            key, val = m.group(1), m.group(2).strip().strip('"').strip("'")
            result[key] = val
    return result


def detect_phase(project_path: Path) -> dict:
    """Detect current phase by scanning project files."""
    story_file = project_path / "story.md"
    volumes_dir = project_path / "volumes"
    chapters_dir = project_path / "chapters"
    archives_dir = project_path / "archives"
    agent_dir = project_path / ".agent"

    state = {
        "current_volume": "",
        "current_chapter": "",
        "current_phase": "setup",
        "project_status": "initializing",
        "last_volume_completed": "false",
        "updated_at": datetime.datetime.now().strftime("%Y-%m-%d"),
    }

    # No story.md → project not created
    if not story_file.exists():
        return state

    state["project_status"] = "planning"

    # Scan volumes
    volume_files = sorted(volumes_dir.glob("volume-*.md")) if volumes_dir.exists() else []
    chapter_files = sorted(chapters_dir.glob("vol-*-ch-*.md")) if chapters_dir.exists() else []

    if not volume_files:
        state["current_phase"] = "setup"
        return state

    # Get latest volume number
    latest_vol = 0
    for vf in volume_files:
        m = re.search(r"volume-(\d+)", vf.name)
        if m:
            latest_vol = max(latest_vol, int(m.group(1)))
    state["current_volume"] = str(latest_vol)

    if not chapter_files:
        state["current_phase"] = "volume"
        return state

    # Scan chapters — find latest by volume and chapter number
    latest_chapter = (0, 0, "")  # (vol, ch, status)
    for cf in chapter_files:
        m = re.search(r"vol-(\d+)-ch-(\d+)", cf.name)
        if not m:
            continue
        vol, ch = int(m.group(1)), int(m.group(2))

        # Read status from file content
        text = cf.read_text(encoding="utf-8")
        status_match = re.search(r"(?m)^status:\s*(\w+)", text)
        ch_status = status_match.group(1) if status_match else "outline"

        key = (vol, ch, CHAPTER_STATUS_ORDER.get(ch_status, -1))
        if key > latest_chapter:
            latest_chapter = key

    if latest_chapter[2]:  # has latest chapter info
        state["current_volume"] = str(latest_chapter[0])
        state["current_chapter"] = str(latest_chapter[1])
    else:
        state["current_phase"] = "volume"
        return state

    _, _, status_idx = latest_chapter

    # All chapters archived → check volume completion
    all_archived = all(
        cf.read_text(encoding="utf-8").find("status: archived") >= 0
        for cf in chapter_files
    )
    if all_archived:
        state["last_volume_completed"] = "true"
        state["project_status"] = "writing"
        # Check if next volume exists
        next_vol = volumes_dir / f"volume-{latest_chapter[0] + 1}.md"
        if next_vol.exists():
            state["current_phase"] = "chapter-loop"  # next volume ready
        else:
            state["current_phase"] = "review"
        return state

    # Determine phase from latest chapter status
    if status_idx == 0:  # outline
        # Check if prompt exists
        prompt_files = list(
            (project_path / "prompts").glob(
                f"vol-{latest_chapter[0]}-ch-{latest_chapter[1]}-prompt.md"
            )
        ) if (project_path / "prompts").exists() else []
        if prompt_files:
            state["current_phase"] = "review"  # prompt verification needed
        else:
            state["current_phase"] = "chapter-loop"
    elif status_idx == 1:  # draft
        draft_files = list(
            (project_path / "archives").glob(
                f"vol-{latest_chapter[0]}-ch-{latest_chapter[1]}-*.draft.md"
            )
        ) if archives_dir.exists() else []
        if draft_files:
            state["current_phase"] = "review"  # body verification needed
        else:
            state["current_phase"] = "chapter-loop"
    elif status_idx == 2:  # archived
        state["current_phase"] = "chapter-loop"

    state["project_status"] = "writing"
    return state


def write_status(agent_dir: Path, state: dict) -> None:
    """Write state to .agent/status.md (Markdown frontmatter format)."""
    agent_dir.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Agent Status",
        "",
        "```yaml",
    ]
    for key in ["current_volume", "current_chapter", "current_phase",
                 "project_status", "last_volume_completed", "updated_at"]:
        lines.append(f"{key}: {state.get(key, '')}")
    lines.append("```\n")

    (agent_dir / "status.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Detect novel project phase")
    parser.add_argument("--project", default=".", help="Project directory (default: CWD)")
    parser.add_argument("--write", action="store_true", help="Write result to .agent/status.md")
    args = parser.parse_args()

    project_path = Path(args.project).resolve()
    agent_dir = project_path / ".agent"

    cache = read_status_cache(agent_dir)
    state = detect_phase(project_path)

    # Override from cache when no chapter info is detected yet
    if not state["current_volume"] and cache.get("current_volume"):
        state["current_volume"] = cache["current_volume"]
    if not state["current_chapter"] and cache.get("current_chapter"):
        state["current_chapter"] = cache["current_chapter"]
    if state["current_phase"] == "setup" and cache.get("current_phase") not in ("setup", "initializing"):
        state["current_phase"] = cache["current_phase"]

    if args.write:
        write_status(agent_dir, state)

    # Output key=value pairs for shell parsing
    for key in ["current_volume", "current_chapter", "current_phase",
                 "project_status", "last_volume_completed", "updated_at"]:
        print(f"{key}={state.get(key, '')}")


if __name__ == "__main__":
    main()
