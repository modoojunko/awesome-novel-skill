# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is **awesome-novel-skilll** — a state-driven AI collaborative novel writing workflow system. It guides authors through world-building, character development, story outlining, and chapter writing using AI agents.

The system is designed for multiple AI tools (DeepSeek TUI, Claude Code, Hermes, OpenClaw) and is primarily used in Chinese.

## Architecture: State-Driven Loop

The core architecture is a **state-driven loop**, NOT a linear pipeline:

```
Step 1 (检测状态) → 匹配路由 → Read 子skill → 执行子task → 更新状态 → 回到 Step 1
```

**Key principle:** The `chapter.md#status` field is the single source of truth for routing decisions. All sub-skills read this status and update it when done.

### Sub-Skills (in skills/)

| Sub-skill | Purpose | Triggers |
|-----------|---------|----------|
| `setup/` | Project init + settings (genre/world/characters) | New project or "discuss settings" |
| `outline/` | Story arc + volume outlines | "plan story arc" / "next volume" |
| `chapter/` | Chapter outline (memo + emotional_design) | Chapter outline phase |
| `prompt/` | Generate writing prompt from chapter outline | status=outline, no prompt exists |
| `prompt-verify/` | Verify prompt quality before writing | status=outline, prompt exists |
| `write/` | Generate actual chapter text | status=draft, no draft exists |
| `body-verify/` | Verify written text quality | status=draft, draft exists |
| `review/` | Deep review (10-dimension diagnosis) | Author requests review |
| `archive/` | Archive chapter, update character states | Author confirms archive |
| `migrate/` | Migrate v2.x projects to v3.0 | story.yaml exists (no story.md) |

### Chapter Status Flow

```
outline → draft → archived
```

Status updates drive the main loop — each sub-skill updates status when complete, causing the main agent to re-detect and route to the next step.

## Key File Conventions

### Project Structure (created by init.py)

```
{project-name}/
├── story.md              # Project index (meta + story_arc)
├── settings/
│   ├── world-setting.md  # Geography/politics/rules
│   ├── writing-style.md  # Writing style config
│   ├── genre-setting.md  # Genre satisfaction types/pacing/taboos
│   └── character-setting/
│       └── {id}.md       # One file per character (append-only state history)
├── volumes/
│   └── volume-{N}.md     # Volume outline (chapters_summary)
├── chapters/
│   └── vol-{N}-ch-{M}.md # Chapter outline (status field drives routing)
├── prompts/
│   └── vol-{N}-ch-{M}-prompt.md  # Generated prompts (overwritable)
└── archives/
    ├── vol-{N}-ch-{M}-{slug}.draft.md  # Draft (in-progress)
    └── vol-{N}-ch-{M}-{slug}.md        # Archived (final)
```

### Critical Invariants

- **chapters/\*.md#status** — Progress marker. Values: `outline` | `draft` | `archived`
- **archives/\*.md** — Final text only lives here. `-draft` suffix = in progress, no suffix = archived
- **character-setting/\*.md** — Append-only. State history entries must equal archived chapter count
- **prompts/\*.md** — Pure generated output, overwritable, not manually maintained

## Important Constraints

**NEVER do these:**
- ❌ Git operations (commit, push, branch)
- ❌ Modify files outside the project directory
- ❌ Install packages or modify system config
- ❌ Skip sub-skill dispatch — always route through sub-skills for project file operations
- ❌ Overwrite character files — append only

**ALWAYS do these:**
- ✅ Read `references/*.md` style guides before writing settings/chapters
- ✅ Check `chapter.md#status` before deciding next action
- ✅ Update `.agent/status.md` after completing sub-skill tasks
- ✅ Use independent verification (body-verify, prompt-verify) before moving to next phase

## Common Workflows

### Starting a New Novel
```
1. Author says: "帮我写本小说"
2. Main agent detects no story.md → dispatches to skills/setup/
3. Setup completes → Phase 2: outline
4. Author says "开始写" → chapter-by-chapter loop begins
```

### Continuing from Last Session
```
1. Author says "继续写" or triggers skill
2. Main agent reads .agent/status.md
3. Reads current chapter.md + volume.md
4. Routes based on status (outline→prompt, draft→write, archived→next)
```

### SOLO Mode
Trigger with "solo" / "单机" / "你全权写". Agent handles everything without stopping for confirmation. Still requires: status updates, file output, quality gates.

## Style Guides (references/)

These define what "good" looks like for each artifact:
- `chapter-quality-checklist.md` — 15-item body verification
- `chapter-setting-style.md` — Chapter outline format + emotional design
- `character-setting-style.md` — 6-layer cognitive model for characters
- `genre-style.md` — Pacing rules, satisfaction types, taboos
- `world-setup-style.md` — Geography/politics/rules structure
- `story-arc-style.md` — Main arc splitting methodology
- `volume-setting-style.md` — Volume outline format
- `prompt-setting-style.md` — Prompt assembly structure

## Model Requirements

- **Phase 1-3 (setup/outline/chapter):** Requires strong reasoning capability (DeepSeek V4 / Claude Sonnet class)
- **Writing phase:** Can use weaker models, quality may vary
- If model is weak: refuse Phase 1-3 execution, prompt user to check model configuration
