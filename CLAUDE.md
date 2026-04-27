# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目性质

这是一个 **Agent Skill 项目**，不是传统应用。它被安装到 `~/.claude/skills/awesome-novel/`（或 `~/.hermes/skills/awesome-novel/`），由 Claude Code 在运行时加载 SKILL.md 作为工作流定义。

修改 SKILL.md 后需重新安装才能生效。

## 安装与测试

```bash
# 安装到 Claude Code / Hermes / OpenClaw
./install.sh claude-code
./install.sh hermes
./install.sh openclaw

# 手动安装（以 Claude Code 为例，其他平台替换路径）
mkdir -p ~/.claude/skills/awesome-novel
cp SKILL.md ~/.claude/skills/awesome-novel/
cp -r scripts ~/.claude/skills/awesome-novel/
```

修改 SKILL.md 或模板后需重新执行 `./install.sh` 才能生效——Agent 加载的是安装路径下的副本，不是仓库源文件。

**测试方式**：
1. 在新目录下启动 Claude Code，对 Agent 说"我想写一本小说"
2. 检查 Agent 是否按 SKILL.md 的 Phase 1→2→3→4→5→6 流程引导
3. 参考 `example/` 目录查看各阶段产物的预期格式

`example/` 目录包含多本测试用小说：

- `example/暗流/` — 都市悬疑，一卷三章，展示了完整 Phase 1→6 流程，含 anti-ai.yaml、hooks.yaml 等新模板。
- `example/守墓人/` — 玄幻题材，两卷三章，旧版示例项目。

## 模板系统

`scripts/init.py` 是唯一的可执行代码。它通过复制 `scripts/templates/` 下的 `.yaml.template` 文件来创建小说项目骨架。

**模板 → 目标映射**（由 init.py 执行）:

| 模板 | 复制到 | 用途 |
|------|--------|------|
| `story.yaml.template` | `{project}/story.yaml` | 项目索引，通过相对路径引用所有子文档 |
| `world-setting.yaml.template` | `{project}/settings/world-setting.yaml` | 世界设定（地理、政治、文化等） |
| `writing-style.yaml.template` | `{project}/settings/writing-style.yaml` | 写作风格指南 + 题材配置（genre）+ 三层技法分发（skill_layers） |
| `anti-ai.yaml.template` | `{project}/settings/anti-ai.yaml` | AI味检测规则：中英文疲劳词 blocklist、句式规则、对话规则、改写算法 |
| `hooks.yaml.template` | `{project}/settings/hooks.yaml` | 伏笔/钩子全生命周期追踪（pending→mentioned→resolved→abandoned） |
| `character.yaml.template` | 不自动复制 | 角色设定模板，讨论阶段由 Agent 按需创建 |
| `volume.yaml.template` | 不自动复制 | 卷模板，故事线拆分阶段由 Agent 按需创建 |
| `chapter.yaml.template` | 不自动复制 | 章节模板，章纲阶段由 Agent 按需创建 |
| `author-intent.md.template` | `{project}/author-intent.md` | 长周期创作方向（核心主题、终局设想、写作信条、伏笔池） |
| `current-focus.md.template` | `{project}/current-focus.md` | 1-3章中期聚焦（优先级、支线、钩子、节奏意图、限制） |

修改模板内容 → 影响后续 `init` 创建的新项目。已有项目不受影响。

## 目录结构

初始化后的项目骨架及 `example/` 参考：

```
project/
├── story.yaml                          # 项目索引（相对路径引用所有子文档）
├── author-intent.md                    # 长周期作者意图（核心主题/终局/信条/伏笔池）
├── current-focus.md                    # 1-3章中期聚焦（优先级/支线/钩子/节奏）
├── settings/
│   ├── world-setting.yaml              # 世界设定
│   ├── writing-style.yaml              # 写作风格指南 + 题材配置 + 三层技法分发
│   ├── anti-ai.yaml                    # AI味检测规则（疲劳词/句式/对话/改写算法）
│   ├── hooks.yaml                      # 伏笔/钩子全生命周期追踪
│   └── character-setting/              # 角色文件（每角色一个 yaml）
├── volumes/                            # 卷文件（卷纲+章节摘要）
├── chapters/                           # 章纲（只放 outline，不放正文）
├── prompts/                            # 提示词（prose .md 格式，非 YAML）
└── archives/                           # 正文（唯一存放处，markdown）
```

## SKILL.md 架构

SKILL.md 定义完整的 6 阶段工作流，是此项目的核心：

1. **Phase 1: Init** — 调用 `scripts/init.py` 创建目录结构（含 anti-ai.yaml、hooks.yaml、control docs）
2. **Phase 2: 设定** — 讨论世界设定 + 角色设定 + 写作风格确认 + 题材选择 + 钩子初始化
3. **Phase 3: 故事线拆分** — 逐卷逐章讨论章纲 + 同步更新 hooks.yaml（埋/提/收钩子）
4. **Phase 4: 提示词生成** — 两轮操作：第一轮视角转换（上帝视角章纲→沉浸式指引），第二轮组装 prose 提示词 + 生成 3 个变体。提示词按 L1/L2 三层技法分发
5. **Phase 5: 正文生成** — subagent 读取 prose 提示词生成正文，主 Agent 执行六项质量检查（含 anti-ai.yaml 疲劳词和句式检测）
6. **Phase 6: 归档** — 正文已在 Phase 5 写入 archives/，更新角色 state_history、hooks.yaml、story.yaml

## 关键约定

**文件职责分离（核心架构原则）**：
- `chapters/` — 只放章纲（outline + status），**禁止放正文**
- `prompts/` — 只放提示词，**.md prose 格式**（非 YAML），5 段结构：角色定位→原则禁忌→故事背景→写作指引→写作要求
- `archives/` — 正文唯一存放处，Phase 5 直接写入，Phase 6 定稿

**流程护栏**：
- 所有 YAML 和正文必须经作者讨论确认后才写入——Agent 是引导者，不能代笔
- Phase 4 视角转换必须先单独经作者确认，确认后才能生成变体
- 提示词必须注入 writing-style 四个字段（role / core_principles / possible_mistakes / depiction_techniques），缺失任何一个 subagent 都会放飞
- 提示词应按 skill_layers 三层分发：L1 结构层→叙事约束，L2 内容层→写作原则段，L3 审查层→保留给 Phase 5
- 禁止用上帝视角章纲直接喂给 subagent——必须先经视角转换
- Phase 5 正文必须通过 anti-ai.yaml 的六项检测（含 AI 疲劳词和句式违规）

**归档约定**：
- 命名: `vol-{N}-ch-{M}-{slugified-title}.md`
- story.yaml 是项目索引，通过相对路径引用子文档
- 角色 state_history 在每次归档时由 Agent 分析正文后自动更新
- hooks.yaml 在每次归档时更新钩子状态（mention/resolve/defer），并执行钩子健康检查
- 默认授权模式为"步步授权"，作者每步确认；可切换为"全部授权"
