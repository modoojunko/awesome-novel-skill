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
cp -r agents ~/.claude/skills/awesome-novel/
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

### 仓库结构

```
awesome-novel-skill/
├── SKILL.md                            # 主 Agent 工作流定义（安装到 skills 目录）
├── agents/                             # 子 Agent 定义（33 个，圆桌 + 流水线）
│   ├── index.md                        # Agent 派发表
│   ├── roundtable/                     # 讨论 Agent（设定/卷纲/章纲/段拆分）
│   └── pipeline/                       # 流水线 Agent（执行 + 验收）
├── scripts/                            # 初始化脚本 + 模板
│   ├── init.py                         # 项目初始化器
│   ├── import.py                       # 小说导入器
│   ├── analyze_style.py                # 文风分析器
│   └── templates/                      # YAML 模板
└── docs/                               # 设计文档
```

### 初始化后的小说项目结构

```
project/
├── story.yaml                          # 项目索引（相对路径引用所有子文档）
├── author-intent.md                    # 长周期作者意图（核心主题/终局/信条/伏笔池）
├── current-focus.md                    # 1-3章中期聚焦（优先级/支线/钩子/节奏）
├── .agent/                             # Agent 活动记录
│   ├── status.md                       # 进度状态
│   ├── roundtables/                    # Q&A + 圆桌讨论记录
│   ├── reviews/                        # 验收报告
│   └── lessons/                        # 跨章节记忆
├── settings/
│   ├── world-setting.yaml              # 世界设定
│   ├── writing-style.yaml              # 写作风格指南 + 题材配置 + 三层技法分发
│   ├── anti-ai.yaml                    # AI味检测规则
│   ├── hooks.yaml                      # 伏笔/钩子全生命周期追踪
│   └── character-setting/              # 角色文件（每角色一个 yaml）
├── volumes/                            # 卷文件（卷纲+章节摘要）
├── chapters/                           # 章纲（只放 outline，不放正文）
├── prompts/                            # 提示词（prose .md 格式）
└── archives/                           # 正文（唯一存放处，markdown）
```

## SKILL.md 架构

SKILL.md 已被重写为**主 Agent 编排器**，不再是单体工作流。核心变更：

1. **主 Agent（pro 模型）**：不创作、不验收、不改文。只做调度和决策。
2. **子 Agent（flash 模型）**：33 个 Agent 分散到 `agents/` 目录，分两类：
   - **圆桌 Agent**（15 个）：设定/卷纲/章纲/段拆分，互看方案、收敛矛盾
   - **流水线 Agent**（17 个）：执行 + 验收，文件传递，5 轮协议
3. **通信**：Agent 之间通过文件传递，不通过对话。主 Agent 只读 status。
4. **记忆**：执行 Agent 在验收通过后自写 `.agent/lessons/`，下次派活时注入。
5. **日间/夜间模式**：白天 3 次→升级作者，夜间→降级+标记。

### 完整流程

```
一次性：
  Step 1 初始化          → exec-init + review-init
  Step 2 设定圆桌        → 5 讨论 Agent 问作者 → 圆桌收敛 → exec 落盘
  Step 3.1 卷纲圆桌       → volume.yaml

每卷循环：
  Step 3.2 章纲圆桌       → N 份 chapter.yaml
  For each chapter:
    Step 3.3 段拆分圆桌    → segment 方案
    Step 4 提示词组装      → exec-prompt + review-prompt
    Step 5 正文 + 去AI味  → exec-prose(并行) → exec-stitch → exec-de-ai → review-prose
    Step 6 归档            → exec-archive + review-archive
```

## 关键约定

**文件职责分离（核心架构原则）**：
- `chapters/` — 只放章纲（outline + status），**禁止放正文**
- `prompts/` — 只放提示词，**.md prose 格式**（非 YAML），5 段结构：角色定位→原则禁忌→故事背景→写作指引→写作要求
- `archives/` — 正文唯一存放处，Phase 5 写入草稿（`-draft` 标记），Phase 6 定稿后去掉 `-draft`

**流程护栏**：
- 所有 YAML 和正文必须经作者讨论确认后才写入——Agent 是引导者，不能代笔
- Phase 4 提示词必须注入 writing-style 四个字段（role / core_principles / possible_mistakes / depiction_techniques），缺失任何一个 subagent 都会放飞
- 提示词应按 skill_layers 三层分发：L1 结构层→叙事约束，L2 内容层→写作原则段，L3 审查层→保留给 Phase 5
- Phase 5 正文必须通过 review-prose 的六项检测（含 anti-ai.yaml 疲劳词和句式违规）
- 5 轮协议：执行→验收循环，第 5 轮仍不一致则升级作者

**归档约定**：
- 草稿命名: `vol-{N}-ch-{M}-{slugified-title}.draft.md`（Phase 5 写入，作者审阅用）
- 定稿命名: `vol-{N}-ch-{M}-{slugified-title}.md`（Phase 6 归档后去掉 `-draft`）
- story.yaml 是项目索引，通过相对路径引用子文档
- 角色 state_history 在每次归档时由 Agent 分析正文后自动更新
- hooks.yaml 在每次归档时更新钩子状态（mention/resolve/defer），并执行钩子健康检查
- 默认授权模式为"步步授权"，作者每步确认；可切换为"全部授权"
