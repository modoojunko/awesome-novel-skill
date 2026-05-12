---
name: awesome-novel
description: 和 AI 协作写小说的工作流系统。流程：一次设定→规划卷纲→逐章写作循环（章纲→自动提示词→正文生成→归档→下一章）。适用场景：从零写新小说、导入已有小说、学习参考文风。
---

# Novel — 小说创作工作流

和 AI 一起写小说。**一次设定**世界观/角色/写作风格 → **主线拆纲+卷纲展开** → **逐章写作循环**（章纲→提示词→正文→验收→归档→下一章）

## 项目目录结构

Agent 在用户当前目录下创建/编辑以下文件：

```
{project-name}/
├── story.md              # ★ 必有：项目索引（元信息/引用路径/主线拆纲）
├── settings/
│   ├── world-setting.md  # 世界观（core: geography/politics/rules, extended: ...）
│   ├── writing-style.md  # 写作风格
│   ├── genre-setting.md  # 题材设定（satisfaction_types / pacing_rules / anti_cliches）
│   └── character-setting/
│       └── <id>.md       # ★ 每角色一个文件（状态历史 + 情绪弧线 追加写入）
├── volumes/
│   └── volume-{N}.md     # 卷纲（chapters_summary 占位章纲）
├── chapters/
│   └── vol-{N}-ch-{M}.md # ★ 章纲唯一存放处（memo + emotional_design + status）
├── prompts/
│   └── vol-{N}-ch-{M}-prompt.md  # ★ 章提示词（自动生成，可覆盖）
└── archives/
    ├── vol-{N}-ch-{M}-{slug}.draft.md  # 草稿（写作中）
    └── vol-{N}-ch-{M}-{slug}.md        # ★ 定稿（归档后去掉 -draft）
```

**关键文件与不变约束：**

- **`chapters/vol-{N}-ch-{M}.md#status`** — ★ 进度真相源。`outline → draft → archived` 驱动 Step 1 路由。归档时更新。
- **`settings/character-setting/<id>.md` → 状态历史** — ★ 角色状态唯一真相源。归档时追加，状态历史条目数必须等于该角色已归档章节数。
- **`archives/vol-{N}-ch-{M}-{slug}.md`** — ★ 正文唯一存放处。文件名有 `-draft` = 未归档，没有 = 已归档。
- **`volume-{N}.md#chapters_summary`** — 卷纲占位章纲，逐章讨论时详情写入 chapter.md。

**约定：**
- `chapters/` 只放章纲 md，不放正文
- `prompts/` 只放提示词 md，**纯生成产物**——可覆盖，不手动维护
- `archives/` 正文唯一存放处
- `settings/character-setting/` 每角色独立 md，追加写入不覆盖
- `volumes/` 卷纲 md，chapters_summary 只写占位章纲（逐章讨论时补充写入 chapter.md）

## 硬性自检协议（贯穿整个 Skill）

下面每个产出完成后，必须先自检 → 修复 → 再汇报/推进：

| 产出 | 生命周期 | 自检清单出处 |
|------|---------|-------------|
| 世界观 | 基础一次性，后续可追加 | `references/world-setup-style.md` |
| 写作风格 + 题材设定 | 一次性（基本不改） | `references/writing-style.md` + `references/genre-style.md` |
| 角色设定 | 基础一次性，后续可追加 | `references/character-setting-style.md` |
| 主线拆纲（story.md 故事主线 + 分卷规划） | 一次性（Phase 2 入口处） | `references/story-arc-style.md` |
| 卷纲（volume-N.md） | 每卷一次 | `references/volume-setting-style.md` |
| 章纲（chapter.md） | 每章一次 | `references/chapter-setting-style.md` |
| 提示词（prompt.md） | 每章一次 | `references/prompt-setting-style.md` |
| 正文（archives/ 定稿） | 每章一次 | `references/chapter-quality-checklist.md` + 深度评审（可选） |

**执行方式（按能力降级，优先用更隔离的方式）：**

1. **Agent Teams（最优）** — 开一个独立的 reviewer agent，给 ta "产出文件路径 + 对应清单 + 关键上下文"，逐项核查并严格汇报结论（哪几条 pass / 哪几条 fail + 证据 + 改写建议）
2. **subAgent（次优）** — 没有 Teams 能力但能开 subagent 就用 subagent 走同样流程
3. **自检（兜底）** — 当前没有上述能力，就自己严格逐项核查——不允许目测一遍就放行

**铁律：** 拿到结论后先按 fail 项把产出改完，再向用户汇报"做完了" + 自检结论 + 改了什么。直接拿原始结论汇报但不修复 = 违规。

## 各阶段文件读取指南

每个子步骤按"输出什么 → 读什么 → 按需加载什么"加载上下文。读完产出，再释放换下一步。

| 子步骤 | 输出什么 | 读什么（必读） | 按需加载 |
|--------|---------|--------------|---------|
| **1.1 新建项目** | 项目骨架 + `story.md` | `scripts/init.py`（创建骨架） | — |
| **1.1 导入已有** | 切分的章纲 + archives/ | `scripts/import.py`（导入切分） | — |
| **1.2 题材选择+风格** | `settings/genre-setting.md`<br>`settings/writing-style.md`（预填） | `references/genre-style.md`（选题指南+验收） | `references/genre-example/` 对应类型（配置参考） |
| **1.3 世界观** | `settings/world-setting.md` | `references/world-setup-style.md`（引导讨论+自检） | — |
| **1.4 角色** | `settings/character-setting/<id>.md` | 已有角色文件（追加时不覆盖）<br>`references/character-setting-style.md`（认知6层+自检） | — |
| **2.0 主线拆纲** | `story.md#story_arc`（主线+分卷） | `references/story-arc-style.md`（从结局倒推法） | `settings/world-setting.md` core（冲突空间参考）<br>角色文件（按需看动机） |
| **2.1 卷纲** | `volumes/volume-{N}.md`（章节列表） | `references/volume-setting-style.md`（指南+自检） | — |
| **3.1 章纲** | `chapters/vol-{N}-ch-{M}.md` | `volumes/volume-{N}.md#chapters_summary`（卷纲给的本章方向）<br>`references/chapter-setting-style.md`（指南+自检） | — |
| **3.2 提示词** | `prompts/vol-{N}-ch-{M}-prompt.md` | `references/prompt-setting-style.md`（提示词指南+模板） | — |
| **3.3 正文生成** | `archives/vol-{N}-ch-{M}-*.draft.md` | `prompts/vol-{N}-ch-{M}-prompt.md`（单一入口） | — |
| **3.4 验收+评审** | 质量检查报告（内存）<br>诊断报告（内存、可选） | `archives/vol-{N}-ch-{M}-*.md`（正文）<br>`references/chapter-quality-checklist.md`（15 项检查） | — |
| **3.5 归档** | `archives/vol-{N}-ch-{M}-*.md`（去 draft）<br>`chapters/vol-{N}-ch-{M}.md`（status→archived）<br>角色状态追加 + `status.md` 更新 | 各角色文件（追加状态历史+情绪弧线） | 最近 3 章 `chapters/`（滑动窗口审视） |

## 主 Agent 运作流程

### Step 1: 检测当前进度

先读 `story.md`。不存在 → 项目未创建，Read `skills/setup/SKILL.md`。

存在 → 读 `.agent/status.md` 获取状态缓存（current_volume、current_chapter、current_phase）。然后交叉验证：
- 读 `chapters/` 下最大章号的 `status` 字段 → 与缓存比对
- 一致 → 快速定位。不一致 → 以实际文件为准更新 status.md

兜底：status.md 不存在 → 回退到目录扫描（volumes/ → chapters/ → status 判断）。

| 信号 | 下一步 |
|------|--------|
| 无 volumes/ 或无 volume md | → `novel-setup`（先完成设定和卷纲）|
| settings/world-setting.md 字段大量为空 | → `novel-setup`（设定未完成）|
| 最新 chapter.md status = `outline` | → 走 Chapter Loop（从章纲开始） |
| 最新 chapter.md status = `draft` | → 走 Chapter Loop（从作者审阅开始。提示词已存在则直接写正文，不存在则自动组装后写） |
| 最新 chapter.md status = `archived` | 本卷还有未归档章？→ 问"下一章继续？"。全部归档 → 卷完成报告 + 选项 |
| 无任何 chapter.md | → 卷纲已定但尚未开始写 → 问"开始写第一章？" |

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
| "归档""存档" | → Chapter Loop 末步自动归档。手动触发时检测最新 chapter.md：`draft` → 走归档 / `archived` → 告知已完成 |
| "评审""评价""review""检查这章""这章怎么样" | 走 `novel-chapter-loop`（3.4 验收含可选深度诊断） |
| "小说进度""第X卷进度" | 只读报告，不分发 |

### Step 3: 前置产出检查

根据目标路由检查前置文件：

| 目标 | 检查项 |
|------|--------|
| novel-volume | story.md story_arc 已定义（至少已完成主线拆纲）、settings/world-setting.md 非模板、settings/writing-style.md 非模板 |
| novel-chapter-loop | volumes/volume-{N}.md 存在且 chapters_summary 非空 |

缺失 → **STOP**。告知作者"XX 还没完成，先补这一环"，路由到前置 Phase 的子技能。

**设定字段优先级（settings/world-setting.md）：**
- core（必填——填完即可进入写作循环）：geography, politics, rules
- extended（可选——按需在写作中追加）：culture, history, physics, biology, sociology

### Step 4: 分发

匹配用户意图后，根据目标路由选择对应子技能，**Read 子技能文件并按其中流程执行**：

| 路由 | 子技能 | 读取路径 |
|------|--------|---------|
| novel-setup | 创建项目 + 设定 | `skills/setup/SKILL.md` |
| novel-style-extract | 文风提取（三步） | `skills/style-extract/SKILL.md` |
| novel-volume | 主线拆纲+卷纲规划 | `skills/outline/SKILL.md`（主线拆纲 + 卷纲部分） |
| novel-chapter-loop | 逐章写作循环 | `skills/chapter-loop/SKILL.md` |

