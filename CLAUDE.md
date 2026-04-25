# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目性质

这是一个 **Agent Skill 项目**，不是传统应用。它被安装到 `~/.claude/skills/awesome-novel/`（或 `~/.hermes/skills/awesome-novel/`），由 Claude Code 在运行时加载 SKILL.md 作为工作流定义。

修改 SKILL.md 后需重新安装才能生效。

## 安装与测试

```bash
# 安装到 Claude Code
./install.sh claude-code

# 安装到 Hermes
./install.sh hermes

# 手动安装（Claude Code）
mkdir -p ~/.claude/skills/awesome-novel
cp SKILL.md ~/.claude/skills/awesome-novel/
cp -r scripts ~/.claude/skills/awesome-novel/
```

测试方式：在新目录下启动 Claude Code，说"create novel test-project"验证 init 流程。

## 模板系统

`scripts/init.py` 是唯一的可执行代码。它通过复制 `scripts/templates/` 下的 `.yaml.template` 文件来创建小说项目骨架。

**模板 → 目标映射**（由 init.py 执行）:

| 模板 | 复制到 | 用途 |
|------|--------|------|
| `story.yaml.template` | `{project}/story.yaml` | 项目索引，通过相对路径引用所有子文档 |
| `world-setting.yaml.template` | `{project}/settings/world-setting.yaml` | 世界设定（地理、政治、文化等） |
| `writing-style.yaml.template` | `{project}/settings/writing-style.yaml` | 写作风格指南（角色定义、核心原则、描写技巧） |
| `character.yaml.template` | 不自动复制 | 角色设定模板，讨论阶段由 Agent 按需创建 |
| `volume.yaml.template` | 不自动复制 | 卷模板，故事线拆分阶段由 Agent 按需创建 |
| `chapter.yaml.template` | 不自动复制 | 章节模板，章纲阶段由 Agent 按需创建 |

修改模板内容 → 影响后续 `init` 创建的新项目。已有项目不受影响。

## SKILL.md 架构

SKILL.md 定义完整的 6 阶段工作流，是此项目的核心：

1. **Init** — 调用 `scripts/init.py` 创建目录结构
2. **设定** — 讨论世界设定 + 角色设定，写入 YAML
3. **故事线拆分** — 逐卷逐章讨论章纲
4. **提示词生成** — 组装上下文生成 3 个提示词变体供选择
5. **正文生成** — subagent 读取提示词 YAML 一次生成完整章节
6. **归档** — 写入 markdown + 更新角色 state_history

过程文件（settings/、volumes/、chapters/）使用 YAML。最终产出（archives/）使用 Markdown。

## 关键约定

- 归档命名: `vol-{N}-ch-{M}-{slugified-title}.md`
- story.yaml 是项目索引，通过相对路径引用子文档，避免数据重复
- 角色 state_history 在每次归档时由 Agent 分析正文后自动更新
- 默认授权模式为"步步授权"，作者每步确认；可切换为"全部授权"
