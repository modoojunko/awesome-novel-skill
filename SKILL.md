---
name: novel
description: 人类与AI协作写小说的工作流系统。当用户提到"写小说""创建小说项目""讨论设定""设计角色""规划章节""写第X章""生成正文""归档""继续写""小说进度"时必须使用。即使只说"帮我写完""下一章怎么写"，也要先加载本技能判断当前进度和路由。
---

# Novel — 小说创作工作流

和 AI 一起写小说。从世界观搭建到正文写作，逐步推进。

**Core principle:** 必须按 Phase 顺序推进。跳过 Phase 等于让 subagent 在没有约束的情况下自行判断故事走向。

## 执行规则

进入下一步前，用 read_file 检查该步骤的产出文件是否存在、字段是否非空。
文件不存在或字段为空 → 报告作者"XX 还没完成，需要先走 YY 技能"。
不要根据记忆判断——必须实际读取文件。

## When to Use

用户说"写小说""创建项目""讨论设定""设计角色""规划章节""写第X章""生成正文""归档""继续写""小说进度"等。

**When NOT to use:** 用户只是想聊小说内容、不需要系统化工作流。

## Anti-Patterns

| 借口 | 现实 |
|------|------|
| "作者说写第一章，我直接生成所有文件" | 必须按 Phase 顺序推进 |
| "差不多就行，不用那么详细" | 缺 memo，subagent 不知道读者在等什么 |
| "视角转换跳过自动质量防护" | Agent 自动执行时仍需跑完整双轮净化和 AI 味自检 |
| "模板我看懂了，直接帮作者填好" | Agent 引导讨论，不代笔填 YAML |

## The Process

### Step 1: 检测当前进度

读取项目根目录的 `story.yaml`。若不存在 → 项目未创建，Read `skills/setup/SKILL.md` 执行 Phase 1。

若存在，读取最近操作的 `chapter.yaml`（按 `story.yaml` 的 chapters 列表找），判断：

| 信号 | 当前 Phase | 下一步 |
|------|-----------|--------|
| world-setting.yaml 字段大量为空 | Phase 2 未完成 | → `novel-setup` |
| chapter.yaml status = `outline`，memo 不完整 | Phase 3 进行中 | → `novel-outline` |
| chapter.yaml status = `outline`，memo 完整，提示词文件不存在 | Phase 3 刚完成——章纲确认后自动执行 Phase 4 | → `novel-outline`（章纲确认后自动拆 segment → 生成提示词 → 更新为 draft） |
| chapter.yaml status = `draft`，正文未归档 | Phase 5/6 待执行 | → `novel-write` 或 `novel-archive`。建议归档前先 `novel-review` |
| chapter.yaml status = `archived` | 本章已完成 | 查 story.yaml 本卷所有章节是否全部 archived：全部完成 → 告知"卷 N 已完成"，给出选项：规划下一卷 / 回顾整卷 / 修改某章。未全部完成 → 问作者：下一章还是回顾？ |

**章状态（chapter.status）:**
- `outline` — 章纲和情绪设计已确认（章纲确认后自动拆 segment + 生成提示词 + 更新为 draft）
- `draft` — 提示词已生成，正文写作/修改中，等待归档
- `archived` — 正文已归档

### Step 2: 匹配用户意图

| 用户说 | 目标 Phase | 子技能 |
|--------|-----------|--------|
| "创建项目""写小说""导入小说" | Phase 1 | `novel-setup` |
| "讨论设定""设计角色""世界观""写作风格" | Phase 2 | `novel-setup` |
| "规划章节""章纲""卷纲""故事线" | Phase 3 | `novel-outline` |
| "学文风""提取风格""学习写作风格""参考小说""分析文风" | Phase 2 增强 | `novel-style-extract` |
| "生成提示词""视角转换" | Phase 4 | `novel-prompt` |
| "写正文""写第X章""继续写""质量检查" | Phase 5 | `novel-write` |
| "归档""存档" | Phase 6 | `novel-archive` |
| "评审""评价""review""检查这章""这章怎么样" | 独立评审 | `novel-review` |
| "小说进度""第X卷进度" | 只读报告 | 本技能直接输出，不分发 |

### Step 3: 跳 Phase 检测

若目标 Phase > 当前 Phase + 1，检查前面 Phase 的产出是否完整：

- 目标 Phase 4 → 已移入 Phase 3 自动执行。手动进入 Phase 4（`novel-prompt`）时检查 memo 是否完整
- 目标 Phase 5 → 检查 `prompts/vol-{N}-ch-{M}-prompt.md` 是否存在。不存在 → 检查 chapter.yaml memo 是否完整：完整 → 路由到 `novel-outline` 走自动生成；不完整 → 告知"章纲未完成"
- 目标 Phase 6 → 检查正文是否已写入 archives/

缺失 → **STOP**。告知作者"XX 还没完成，先补这一环"，路由到前置 Phase 的子技能。

### Step 4: 模型门禁

对照下方「模型门禁（MODEL-GATE）」表，检查目标 Phase 的主会话模型要求。若不满足 → **STOP**，告知用户切换模型后再继续。满足要求 → 进入 Step 5。

### Step 5: 分发

匹配用户意图后，根据目标 Phase 选择对应子技能，**Read 子技能文件并按其中流程执行**：

| 目标 Phase | 子技能 | 读取路径 |
|-----------|--------|---------|
| Phase 1+2 | novel-setup — 初始化、世界观、角色、全局提示词 | `skills/setup/SKILL.md` |
| Phase 2 增强 | novel-style-extract — 从参考小说提取文风，三步流程 | `skills/style-extract/SKILL.md` |
| Phase 3 | novel-outline — 卷纲、章纲、memo、情绪设计、卷提示词 | `skills/outline/SKILL.md` |
| Phase 4（手动） | novel-prompt — 手动调整提示词。正常流程已在章纲确认后自动执行 | `skills/prompt/SKILL.md` |
| Phase 5 | novel-write — 单 subagent 写全章、质量检查+深度评审 | `skills/write/SKILL.md` |
| Phase 6 | novel-archive — 归档、角色更新、钩子更新、滑动窗口审视 | `skills/archive/SKILL.md` |
| 独立评审 | novel-review — 10 维 60+ 细项诊断 | `skills/review/SKILL.md` |

子技能文件位于主技能安装目录的 `skills/` 下，即 `~/.claude/skills/awesome-novel/skills/{name}/SKILL.md`。

## 模型门禁（MODEL-GATE）

```
深度推理阶段（Phase 1-4）→ 主会话必须使用 sonnet。
若不满足 → STOP，告知用户切换模型后再继续。不得在 haiku 下执行深度推理。
```

| Phase | 子技能 | 主会话模型 | 原因 |
|-------|--------|-----------|------|
| 1+2 | novel-setup | **sonnet（强制）** | 世界观讨论、角色设计、风格确认——需要深度思考 |
| 2 | novel-style-extract（主 Agent 调度） | **sonnet（强制）** | 风格分析、规则合并——需要深度推理 |
| 2 | novel-style-extract（subagent 定性分析） | sonnet | 分层阅读 + 6 维分析——需要深度理解 |
| 3 | novel-outline | **sonnet（强制）** | 章纲规划、情绪设计、结构推理 |
| 4 | novel-prompt | **sonnet（强制）** | 视角转换、segment 拆分、提示词组装——最耗推理 |
| 5 | novel-write（主 Agent 调度） | haiku 可 | 单 agent 写全章、质量检查——机械操作 |
| 5 | novel-write（subagent 写作） | 从 `writing_model` 读取 | 正文生成，默认 haiku。对质量要求高的章节可改为 sonnet |
| 6 | novel-archive | haiku 可 | 归档、状态更新——机械操作 |
| review | novel-review（主 Agent） | haiku 可 | 主 Agent 已持有全部上下文，直接对照检查——无 subagent 开销 |

**模型切换方法：**
- Claude Code: 输入 `/model` 选择 sonnet，或按 `Alt+T` 切换
- OpenClaw / Hermes: 使用平台模型切换机制，或留空使用默认

## 授权模式

- **步步授权（默认）**：每步需作者确认
- **全部授权**：Agent 全权决定

作者随时说"你全权决定"或"每步都要我确认"切换。子技能继承此模式。

## Bundled Resources

| 路径 | 用途 | 何时读取 |
|------|------|---------|
| `scripts/init.py` | 创建项目骨架 | Phase 1 新建项目时执行 |
| `scripts/import.py` | 导入已有小说，切分章节 | Phase 1 导入模式时执行 |
| `scripts/analyze_style.py` | 参考小说文风统计分析（12 项量化指标） | novel-style-extract Step 1 时执行 |
| `scripts/templates/` | YAML 模板（world-setting、character、writing-style、hooks 等） | 新建项目时 init.py 自动复制；Phase 2 讨论设定时参考字段结构 |
| `genre-corpus/` | 类型档案（24 种预置类型，7 个基类 + 变体覆盖） | Phase 2 设定阶段选择类型档案；Phase 4 提示词注入 prompt_segment |
