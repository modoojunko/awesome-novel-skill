# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目性质

Agent Skill 项目，非传统应用。安装到 `~/.claude/skills/awesome-novel/`，由 Claude Code 在运行时加载 SKILL.md 作为工作流定义。

修改 SKILL.md / 脚本 / 模板后需 `./install.sh <platform>` 才能生效（Agent 加载的是安装路径下的副本，不是仓库源文件）。

## 安装

```bash
./install.sh claude-code   # → ~/.claude/skills/awesome-novel/
./install.sh hermes        # → ~/.hermes/skills/awesome-novel/
./install.sh openclaw      # → ~/.openclaw/skills/awesome-novel/
./install.sh deepseek-tui  # → ~/.deepseek/skills/awesome-novel/
```

install.sh 使用 include list 复制：SKILL.md + scripts/ + skills/ + genre-corpus/ + agents/。

## 架构概览

### 入口：SKILL.md

SKILL.md 是 6 阶段工作流的定义入口，不包含执行细节。它负责：
1. 检测当前项目进度（读 story.yaml + chapter.yaml status）
2. 匹配用户意图到目标 Phase
3. 跳 Phase 检测（检查前置产出是否存在）
4. 模型门禁检查（Phase 1-4 强制 sonnet）
5. 分发到对应子技能

### 子技能系统（skills/）

每个子技能是一个独立的 `skills/{name}/SKILL.md`，由主 SKILL.md 分发执行：

| 子技能目录 | 用途 | 主会话模型 |
|-----------|------|-----------|
| `skills/setup/` | Phase 1+2：初始化、世界观、角色、全局提示词 | sonnet 强制 |
| `skills/style-extract/` | Phase 2 增强：从参考小说提取文风（三步：量化→定性→合并） | sonnet 强制 |
| `skills/outline/` | Phase 3：卷纲、章纲、memo、情绪设计 | sonnet 强制 |
| `skills/prompt/` | Phase 4：手动调整提示词（正常流程自动执行） | sonnet 强制 |
| `skills/write/` | Phase 5：subagent 生成正文 + 主 Agent 检查 | haiku 可 |
| `skills/archive/` | Phase 6：归档、角色状态更新、钩子追踪、滑动窗口审视 | haiku 可 |
| `skills/review/` | 独立评审：10 维 60+ 细项诊断 | haiku 可 |

### 题材语料库（genre-corpus/）

24 种预置类型，通过继承模式组织：

- `index.yaml` — 所有 24 种类型的注册表，每个条目指向一个 base `corpus` 文件
- 基类文件（7 个）：`xianxia.yaml`, `urban.yaml`, `historical.yaml`, `xuanhuan.yaml`, `suspense-crime.yaml`, `scifi-apocalypse.yaml`, `western-fantasy.yaml`, `derivative.yaml`
- `variant/` — 同名文件覆盖基类差异字段（如 `urban-brained.yaml` 叠加到 `urban.yaml`）

每个 corpus 文件包含：`role_override`, `style_blueprint`, `genre_taboos`, `prompt_segment`, `genre_config`, `story_arc_templates`。Phase 4 组装提示词时注入 `prompt_segment`。

### AI 味检测体系

三层检测，数据来源于两个规范文件：

**疲劳词检测** — 中英文 blocklist，写在 `anti-ai.yaml.template` 中，分副词/动词/形容词/连接词/身体反应等类别

**句式规则检测** — `tic-patterns.yaml` 定义 8 种结构性句式模式（"不是而是句式""身体部位情绪模板"等），每个模式有 pattern + threshold + severity。`analyze_style.py` 和 `anti-ai.yaml.template` 共从此文件读取

**改写算法** — `anti-ai.yaml.template` 中定义感知词（看到/听到/闻到/感到等）的移除策略 + 中文"了"的净化逻辑

### 脚本

| 脚本 | 用途 | 何时调用 |
|------|------|---------|
| `scripts/init.py` | 创建项目骨架（复制模板 + 建目录） | Phase 1 新建项目 |
| `scripts/import.py` | 导入已有小说（按章节标记切分 + 写入 archives/ + 创建章纲 yaml） | Phase 1 导入模式 |
| `scripts/analyze_style.py` | 12 项量化文风指标（句长分布、对话比、标点谱、词频、成语密度、形容词副词密度、描写比、身体情绪密度、结构句式、段首多样性等） | novel-style-extract Step 1 |
| `scripts/check_completeness.py` | 扫描项目 YAML，标记空字段和缺失文件 | Phase 3→4 过渡的完整性检查 |

### 模板系统（scripts/templates/）

| 模板 | 目标 | 用途 |
|------|------|------|
| `story.yaml.template` | `{project}/story.yaml` | 项目索引，通过相对路径引用所有子文档 |
| `world-setting.yaml.template` | `settings/world-setting.yaml` | 世界设定（8 个子字段：geography/politics/culture/history/rules/physics/biology/sociology） |
| `writing-style.yaml.template` | `settings/writing-style.yaml` | 4 个必需字段：role/core_principles/possible_mistakes/depiction_techniques + genre 配置 + skill_layers 三层分发 |
| `anti-ai.yaml.template` | `settings/anti-ai.yaml` | AI 味检测规则：blocklist / 句式规则 / 对话规则 / 改写算法 |
| `hooks.yaml.template` | `settings/hooks.yaml` | 伏笔/钩子生命周期（pending→mentioned→resolved→abandoned） |
| `author-intent.md.template` | `author-intent.md` | 长周期创作方向（核心主题、终局设想、写作信条、伏笔池） |
| `current-focus.md.template` | `current-focus.md` | 1-3 章中期聚焦（优先级、支线、钩子、节奏意图、限制） |

### 文件职责分离（核心架构原则）

- `chapters/` — 只放章纲（outline + status），**禁止放正文**
- `prompts/` — 只放提示词，**.md prose 格式**（非 YAML），包含共享约束 + 逐段叙事指引
- `archives/` — 正文唯一存放处。草稿命名 `vol-{N}-ch-{M}-{slug}.draft.md`，定稿去掉 `-draft`

## 关键流程护栏

- 所有 YAML 和正文必须经作者讨论确认后才写入
- Phase 4 视角转换必须先经作者确认，确认后才能组装章提示词
- 提示词必须注入 writing-style 四个字段（role/core_principles/possible_mistakes/depiction_techniques），缺失任何一个 subagent 都会放飞
- 提示词按 skill_layers 三层分发：L1 结构层→叙事约束，L2 内容层→写作原则段，L3 审查层→保留给 Phase 5
- 禁止用上帝视角章纲直接喂给 subagent——必须先经视角转换
- Phase 5 正文必须通过 15 项质量检查（含 AI 疲劳词和句式违规）+ 10 维深度评审

## 命名约定

- 草稿: `vol-{N}-ch-{M}-{slugified-title}.draft.md`
- 定稿: `vol-{N}-ch-{M}-{slugified-title}.md`
- 章纲: `vol-{N}-ch-{M}.yaml`
- 提示词: `vol-{N}-ch-{M}-prompt.md`
- 章状态: `outline` → `draft` → `archived`
