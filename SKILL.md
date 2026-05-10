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

读取项目根目录的 `story.yaml`。若不存在 → 项目未创建，Read `skills/setup/SKILL.md`。

若存在：

1. 读 `volumes/` 目录，找到最大卷号 → 当前卷
2. 读 `chapters/` 目录，筛选当前卷的章节文件，按 chapter 号排序
3. 取最大 chapter 号的 `chapter.yaml`，读 status：

| 信号 | 下一步 |
|------|--------|
| 无 volumes/ 或无 volume yaml | → `novel-setup`（先完成设定和卷纲）|
| world-setting.yaml 字段大量为空 | → `novel-setup`（设定未完成）|
| 最新 chapter.yaml status = `outline` | → 走 Chapter Loop（从情节方向提案开始） |
| 最新 chapter.yaml status = `draft` | → 走 Chapter Loop（从作者审阅开始。提示词已存在则直接写正文，不存在则自动组装后写） |
| 最新 chapter.yaml status = `archived` | 本卷还有未归档章？→ 问"下一章继续？"。全部归档 → 卷完成报告 + 选项 |
| 无任何 chapter.yaml | → 卷纲已定但尚未开始写 → 问"开始写第一章？" |

**章状态（chapter.status）:**
- `outline` — 章纲已定但提示词尚未生成（Chapter Loop 执行中）
- `draft` — 提示词已生成，正文写作/修改中，等待归档
- `archived` — 正文已归档

### Step 2: 匹配用户意图

| 用户说 | 路由 |
|--------|------|
| "创建项目""写小说""导入""讨论设定""设计角色""世界观""写作风格" | Phase 1 `novel-setup` |
| "学文风""提取风格""学习写作风格""参考小说""分析文风" | 增强 `novel-style-extract` |
| "规划卷纲""定卷""下一卷""故事线" | Phase 2 `novel-volume` |
| "写正文""写第X章""继续写""下一章""继续""规划章节""章纲" | Phase 3 `novel-chapter-loop` |
| "归档""存档" | → Chapter Loop 末步自动归档。手动触发时检测最新 chapter.yaml：`draft` → 走归档 / `archived` → 告知已完成 |
| "评审""评价""review""检查这章""这章怎么样" | Phase 4 `novel-review` |
| "小说进度""第X卷进度" | 只读报告，不分发 |

### Step 3: 前置产出检查

根据目标路由检查前置文件：

| 目标 | 检查项 |
|------|--------|
| novel-volume | settings/world-setting.yaml 非模板、writing-style.yaml 非模板 |
| novel-chapter-loop | volume-N.yaml 存在且 chapters_summary 非空 |
| novel-review | archives/ 下存在正文文件 |

缺失 → **STOP**。告知作者"XX 还没完成，先补这一环"，路由到前置 Phase 的子技能。

**设定字段优先级（world-setting.yaml）：**
- core（必填——填完即可进入写作循环）：geography, politics, rules
- extended（可选——按需在写作中追加）：culture, history, physics, biology, sociology

### Step 4: 模型门禁

对照下方「模型门禁（MODEL-GATE）」表，检查目标 Phase 的主会话模型要求。若不满足 → **STOP**，告知用户切换模型后再继续。满足要求 → 进入 Step 5。

### Step 5: 分发

匹配用户意图后，根据目标路由选择对应子技能，**Read 子技能文件并按其中流程执行**：

| 路由 | 子技能 | 读取路径 |
|------|--------|---------|
| novel-setup | 创建项目 + 设定 | `skills/setup/SKILL.md` |
| novel-style-extract | 文风提取（三步） | `skills/style-extract/SKILL.md` |
| novel-volume | 卷纲规划 | `skills/outline/SKILL.md`（卷纲部分） |
| novel-chapter-loop | 逐章写作循环 | `skills/chapter-loop/SKILL.md` |
| novel-review | 深度评审 | `skills/review/SKILL.md` |

子技能文件位于主技能安装目录的 `skills/` 下，即 `~/.claude/skills/awesome-novel/skills/{name}/SKILL.md`。

## 模型门禁（MODEL-GATE）

```
深度推理阶段（Phase 1-3）→ 主会话必须使用 sonnet。
若不满足 → STOP，告知用户切换模型后再继续。不得在 haiku 下执行深度推理。
```

| Phase | 子技能 | 主会话模型 | 原因 |
|-------|--------|-----------|------|
| 1 | novel-setup | **sonnet（强制）** | 设定讨论——需要深度思考 |
| 2 | novel-volume | **sonnet（强制）** | 卷纲规划——需要结构推理 |
| 3 | novel-chapter-loop | **sonnet（强制）** | 情节提案、章纲、视角转换——核心推理 |
| 3 | novel-chapter-loop（subagent 写作） | 从 `writing_model` 读取 | 正文生成，默认 haiku |
| 4 | novel-review | haiku 可 | 主 Agent 已持有全部上下文 |
| — | novel-style-extract | **sonnet（强制）** | 风格分析——需要深度推理 |

**模型切换方法：**
- Claude Code: 输入 `/model` 选择 sonnet，或按 `Alt+T` 切换
- OpenClaw / Hermes / DeepSeek TUI: 使用平台模型切换机制，或留空使用默认

## 授权模式

- **步步授权（默认）**：每步需作者确认
- **全部授权**：Agent 全权决定

作者随时说"你全权决定"或"每步都要我确认"切换。子技能继承此模式。

## Bundled Resources

| 路径 | 用途 | 何时读取 |
|------|------|---------|
| `scripts/init.py` | 创建项目骨架 | Phase 1 新建项目时执行 |
| `scripts/import.py` | 导入已有小说，切分章节 | Phase 1 导入模式时执行 |
| `scripts/templates/` | YAML 模板（world-setting、character、writing-style、hooks 等） | 新建项目时 init.py 自动复制；Phase 2 讨论设定时参考字段结构 |
| `genre-corpus/` | 类型档案（24 种预置类型，自包含文件） | Phase 2 设定阶段选择类型档案；Phase 3 提示词注入 prompt_segment |
