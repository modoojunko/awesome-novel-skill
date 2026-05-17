<p align="center">
  <strong>Novel Agent</strong><br>
  <em>Write Novels with AI — Free, Native DeepSeek V4 Support</em>
</p>

<p align="center">
  <a href="https://github.com/hust-open-atom-club/DeepSeek-TUI"><img src="https://img.shields.io/badge/DeepSeek%20V4-%E2%9C%93%20%E6%94%AF%E6%8C%81-4FC08D?style=flat-square" alt="DeepSeek V4 TUI"></a>
  <a href="https://docs.anthropic.com/en/docs/claude-code/overview"><img src="https://img.shields.io/badge/Claude%20Code-%E2%9C%93%20%E6%94%AF%E6%8C%81-6B46C1?style=flat-square" alt="Claude Code"></a>
  <a href="https://github.com/hermes/hermes"><img src="https://img.shields.io/badge/Hermes-%E2%9C%93%20%E6%94%AF%E6%8C%81-FF6B6B?style=flat-square" alt="Hermes"></a>
  <a href="https://github.com/openclaw/openclaw"><img src="https://img.shields.io/badge/OpenClaw-%E2%9C%93%20%E6%94%AF%E6%8C%81-FFA94D?style=flat-square" alt="OpenClaw"></a>
  <br>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-GPL%203.0-blue?style=flat-square" alt="GPL 3.0"></a>
</p>

> **Free for personal use** — This Skill is completely free for personal users.<br>
> **Commercial use** — Please contact the author for licensing.

Let AI be your novel writing partner, from world-building to character development, from chapter planning to prose writing — guiding you through completing an entire novel step by step.

## What You Need

- A computer with one of: [DeepSeek TUI (DeepSeek V4)](https://github.com/hust-open-atom-club/DeepSeek-TUI), [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview), [Hermes](https://github.com/hermes/hermes), or [OpenClaw](https://github.com/openclaw/openclaw)
- About 1 minute to install

> **Tip**: DeepSeek V4 via DeepSeek TUI is completely free with no API costs.

## Installation

Copy the command for your tool and paste it in your terminal:

### DeepSeek V4 (DeepSeek TUI)

```bash
git clone https://github.com/modoojunko/awesome-novel-skill.git && cd awesome-novel-skill && ./install.sh deepseek-tui
```

### Claude Code

```bash
git clone https://github.com/modoojunko/awesome-novel-skill.git && cd awesome-novel-skill && ./install.sh claude-code
```

### Hermes

```bash
git clone https://github.com/modoojunko/awesome-novel-skill.git && cd awesome-novel-skill && ./install.sh hermes
```

### OpenClaw

```bash
git clone https://github.com/modoojunko/awesome-novel-skill.git && cd awesome-novel-skill && ./install.sh openclaw
```

Manual installation (using DeepSeek V4 as example):

```bash
git clone https://github.com/modoojunko/awesome-novel-skill.git
cd awesome-novel-skill
mkdir -p ~/.deepseek/skills/awesome-novel
cp SKILL.md ~/.deepseek/skills/awesome-novel/
cp -r scripts ~/.deepseek/skills/awesome-novel/
```

> Claude Code users: use `~/.claude/skills/awesome-novel`. Hermes users: use `~/.hermes/skills/awesome-novel`. OpenClaw users: use `~/.openclaw/skills/awesome-novel`.

You'll see "安装完成" (Installation complete) when done.

## Start Writing

After installation, open your terminal in the directory where you want your novel project and launch your AI tool. Then say:

> **"帮我写本小说"** (Help me write a novel)

The Agent will guide you through the rest. Here's the complete flow:

### One-Time Setup

On first novel, the Agent discusses these areas. **No need to decide everything at once** — skip what you don't know and fill in later:

1. **Genre** — Xianxia, urban, mystery, historical... just say what you have in mind. Agent auto-configures writing style and pacing templates based on genre
2. **World Setting** — What world does the story take place in? Any special rules? (e.g., "cultivation world where spiritual roots determine talent")
3. **Main Characters** — Who's the protagonist? What kind of person are they? Agent discusses personality, abilities, and growth history for each character
4. **Writing Style** — Prefer more description or more dialogue? More classical or modern tone? Can also import a novel you like to extract its style

### Planning the Story Framework

After setup, Agent helps plan the overall story structure:

1. **Story Arc Split** — One sentence describing the core conflict of the entire book, then work backward from the ending to break it into major phases
2. **Volume Planning** — Each phase is a volume; what's the content and stopping point of each volume
3. **First Volume Chapters** — How many chapters in volume one and what's the core content of each

> **Don't know the ending?** Tell Agent "I only know the beginning" and it will still help plan the first volume.

### Chapter Writing Loop

Each chapter follows this flow, Agent auto-advances:

| Step | What Happens |
|------|--------------|
| **① Chapter Outline** | Agent gives chapter plan — what to write, how many sections, how emotions flow. Review and say "ok" or "change this" |
| **② Prompt** | Auto-assemble writing prompt from outline and global settings |
| **③ Write** | Agent writes the complete chapter from the prompt |
| **④ Review** | Read through. Say "archive" if satisfied, or "revise paragraph X" / "rewrite" if not |
| **⑤ Archive** | After confirmation, chapter is officially archived. Character status auto-updates, ready for next chapter |

After chapter one, Agent asks "下一章继续吗？" (Continue to next chapter?)

### Automation

- **AI Flavor Removal**: Prompt generation auto-cleans "analysis tone"; after writing, scans for sentence repetition, body reaction templates, and machine-phrase vocabulary (like "cannot help but", "unconsciously") — flags for your decision
- **Foreshadow Tracking**: Emotional hooks at chapter ends auto-tracked; reminders when it's time to pay off
- **Character Status Management**: Location changes, ability growth, relationship shifts — auto-recorded, Agent knows latest state when writing next chapter
- **Pacing Check**: Alert if 3+ consecutive high-tension chapters or 2+ consecutive平淡 chapters

### Common Commands

| You Say | AI Does |
|---------|---------|
| "帮我写本小说" | Create project from scratch + start setting discussion |
| "帮我继续写" | Resume from last progress |
| "写下一章" | Start writing latest chapter |
| "改一下第 X 段" | Revise specified paragraph |
| "这章写完了" or "归档" | Confirm chapter complete |
| "看看进度" | View current progress |
| "导入这本小说" | Import existing draft to continue writing |
| "迁移项目" | Auto-migrate from 2.x to 3.0 format |
| "solo" or "你全权写" | Enter fully automatic mode without stop points |

## Three Collaboration Modes

| Mode | Trigger | Behavior |
|------|---------|----------|
| **Step-by-Step** (default) | — | Waits for your confirmation at each step |
| **Full Delegation** | "你全权决定" | Process nodes still exist, Agent confirms on your behalf |
| **SOLO Mode** | "solo" / "单机" | Simplified flow, no stop points, Agent completes all creative and writing work alone. Great for letting AI go wild |

You can switch modes anytime by telling the Agent.

## Advanced Features

### Pre-built Genre Profiles

Don't want to set up writing style from scratch? The project includes 24 built-in genre profiles — pick one and start immediately. Each profile includes character archetype tendencies, narrative tone, and chapter prompt templates. Covers Xianxia, urban, mystery, historical, sci-fi post-apocalyptic, Western fantasy, and more.

Agent asks if you want to choose one during setup.

### Learn Style from Novels You Love

Have a novel you love and want AI to write in that style?

1. Put the reference novel file in the project directory
2. Tell Agent "分析一下这本小说的文风" (Analyze this novel's style)
3. Agent runs statistical analysis (sentence length, dialogue ratio, description density), then qualitatively extracts style features, outputs a style profile for your confirmation
4. After confirmation, auto-merges into writing config; all subsequent chapters follow this style

## FAQ

**Q: I'm not a programmer, can I install it?**

Yes. Just copy and paste those commands into your terminal. The only requirement is having DeepSeek TUI, Claude Code, Hermes, or OpenClaw installed.

**Q: Do I need a Claude subscription to use this?**

No. DeepSeek V4 (DeepSeek TUI) provides complete functionality for free with no subscriptions or API costs.

**Q: I upgraded the skill, how do I migrate my existing novel projects to the new format?**

When you launch in the current project directory after an upgrade, Agent auto-detects the old format and guides you through migration. Core logic: old files moved entirely to `old/` directory for backup, new project skeleton initialized in place, then old format settings converted field by field to new format. Archived prose copied directly; work-in-progress not migrated. You can manually delete `old/` after confirming migration is correct.

**Q: Can I change settings mid-writing?**

Yes. Just tell Agent "改一下世界观里的 XXX" (Change XXX in world setting) or "这个角色的性格我想调整" (I want to adjust this character's personality) and it will update for you.

**Q: Generated text has AI flavor, what do I do?**

Default config is "low AI flavor" — common machine phrases prohibited ("cannot help but", "unconsciously", "at this moment", "not X but Y" analysis tone), forced alternation between short and long sentences, body reaction templating banned. Auto-scan runs after writing.

**Q: Can I use my own writing style?**

Yes. After project creation, there's a writing style file where you can write in your preferences, and all subsequent chapters will follow this style.

## Star History

<a href="https://star-history.com/#modoojunko/awesome-novel-skill">
  <img src="https://api.star-history.com/svg?repos=modoojunko/awesome-novel-skill&type=date" alt="Star History">
</a>

## Acknowledgments

Thanks to [@hust-open-atom-club](https://github.com/hust-open-atom-club) for [DeepSeek TUI](https://github.com/hust-open-atom-club/DeepSeek-TUI), providing free and smooth terminal experience for DeepSeek V4 users, making this Skill completely free for personal use.

Part of this project's design was inspired by [InkOS](https://github.com/Narcooo/inkos) — including AI flavor detection system, foreshadowing/hook tracking, genre configuration, and layered technique models. Thanks to [@Narcooo](https://github.com/Narcooo) for the excellent work.