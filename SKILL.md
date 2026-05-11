---
name: awesome-novel
description: 和 AI 协作写小说的工作流系统。流程：一次设定→规划卷纲→逐章写作循环（方向提案→章纲→自动提示词→正文生成→归档→下一章）。适用场景：从零写新小说、导入已有小说、学习参考文风。
---

# Novel — 小说创作工作流

和 AI 一起写小说。**一次设定**世界观/角色/写作风格 → **主线拆纲+卷纲展开**（总主线→拆几卷→每卷冲突，再逐卷展开）→ **逐章写作循环**（方向提案→章纲→自动提示词→正文生成→质量门禁→归档→下一章）。每一章都是独立的"提案→确认→生成→检查"闭环，不批量作业。产出物 = 按卷/章拆分的小说正文 + 角色状态追踪。

## 适用场景

"帮我写本小说" —— 从零开始，需要搭世界观和角色
"帮我继续写" —— 已有项目，接着上一章写
"导入这本小说继续写" —— 已有草稿文件，反向提取设定
"学这本小说的文风" —— 参考范文提取风格规则并注入项目
本 Skill 是创作方法论 + AI 协作流程。每本小说有自己的题材、风格和结构，流程提供骨架但不替代作者的创意决策。

## 核心原则

**必须按 Phase 顺序推进。** 跳过 Phase 等于让 subagent 在没有约束的情况下自行判断故事走向。

## 工作流总览

```
Phase 1   设定
   1.1  项目初始化（新建 / 导入）
   1.2  世界观搭建（8 字段逐项讨论）
   1.3  角色设定（每角色独立 yaml）
   1.4  写作风格确认（默认 / 参考范文提取）
   1.5  类型档案选择（24 种预置题材）
   1.6  题材配置（爽点/节奏/反套路）
   1.7  钩子初始化
   1.8  全局提示词生成
   ▼
[Checkpoint Setup]   ← 必须停。确认以下设定全部到位：
                      □ 世界观 core 字段已填（geography / politics / rules）
                      □ 主要角色 yaml 已创建，story_role 已分配
                      □ 写作风格已确认（默认或提取）
                      □ 题材类型已选定，genre_config 已配置
                      ↓ 任意一项缺失 → 返回 Phase 1 补全
   ▼
Phase 2   主线拆纲 + 卷纲展开
   2.0  主线拆纲（总主线 → 拆几卷 → 每卷核心冲突）
   2.1  卷方向确定（角色发声 / 结构模板）
   2.2  卷纲讨论（核心冲突 + 章节列表）
   2.3  卷提示词生成
   ▼
[Checkpoint Volume]  ← 必须停。确认以下卷纲已就绪：
                      □ story_arc 已定义（主线一句话 + 分卷规划：总卷数、每卷冲突）
                      □ 卷方向确定（角色发声分析完成 / 结构模板选定）
                      □ 核心冲突已明确定义
                      □ 章节列表完整（占位章纲已写入）
                      ↓ 任意一项缺失 → 返回 Phase 2 补全
   ▼
Phase 3   逐章写作循环
   3.1  情节方向提案（3-4 个方向）
   ▼
   [硬节点] 作者选择方向 ← 不可跳过。方向不定不进章纲
   ▼
   3.2  章纲（memo 7 段 + 情绪设计 + hooks）
   ▼
   [Checkpoint 章纲]  ← 必须停。确认章纲完整：
                      □ memo 7 段全部有值（悬念/节奏/情绪/视角/对话/描写/落点）
                      □ emotional_design 已填写（情绪状态/强度/弧线方向）
                      □ hooks 已标注（本章铺设/收束的钩子）
                      □ AI 味自检已通过
                      ↓ 任意一项缺失 → 返回 3.2 补全
   ▼
   3.3  自动生成提示词（视角转换 + segment 拆分）
   ▼
   [Checkpoint 提示词] ← 必须停。确认提示词正确：
                      □ 视角转换已完成（非上帝视角章纲）
                      □ segment 拆分合理（每段叙事功能明确）
                      □ writing-style 四字段已注入（role / core_principles / possible_mistakes / depiction_techniques）
                      □ 类型 prompt_segment 已追加
                      ↓ 不满意 → 手动调整或返回 3.3 重新生成
   ▼
   3.4  正文生成 + 质量门禁（15 项检查）
   ▼
   [硬节点] 作者审阅 ← 不可跳过。作者不满意不归档
   ▼
   [Checkpoint Quality]  ← 必须停。确认以下全部通过：
                      □ 15 项正文质量检查通过（含 AI 味检测）
                      □ 作者审阅满意
                      ↓ 不满意 → 回到 3.4 修改。满意才归档
   ▼
   3.6  归档（角色状态 + 钩子追踪 + 滑动窗口）
   3.7  下一章决策 → 回到 3.1（循环）

   第 1 章走完整流程（强制锚点），第 2~N 章重复 3.1→3.7 直到卷内全部章节归档。
   卷完成 → 回到 Phase 2 规划下一卷，或 Phase 1 新增角色/设定。
   所有卷完成 → 全书完结。

   **Phase 不是死锁——卷纲/章纲阶段可随时新增角色或补充设定。**
   设定是活的：故事展开发现需要新角色，随时回 Phase 1 加。
```

## 项目目录结构

Agent 在用户当前目录下创建/编辑以下文件：

```
{project-name}/
├── story.md              # ★ 必有：项目索引（元信息/引用路径/主线拆纲）
├── settings/
│   ├── world-setting.yaml  # 世界观（core: geography/politics/rules, extended: ...）
│   ├── writing-style.yaml  # 写作风格
│   ├── genre-setting.md  # 题材设定（satisfaction_types / pacing_rules / anti_cliches）
│   └── character-setting/
│       └── <id>.yaml       # ★ 每角色一个文件（state_history + emotional_arc 追加写入）
├── volumes/
│   └── volume-{N}.yaml     # 卷纲（chapters_summary 占位章纲）
├── chapters/
│   └── vol-{N}-ch-{M}.yaml # ★ 章纲唯一存放处（memo + emotional_design + hooks + status）
├── prompts/
│   ├── global-prompt.md    # Phase 1 产出：写作方法论汇总（作者参考）
│   └── vol-{N}-ch-{M}-prompt.md  # ★ 章提示词（自动生成，可覆盖）
└── archives/
    ├── vol-{N}-ch-{M}-{slug}.draft.md  # 草稿（写作中）
    └── vol-{N}-ch-{M}-{slug}.md        # ★ 定稿（归档后去掉 -draft）
```

**关键文件与不变约束：**

- **`chapters/vol-{N}-ch-{M}.yaml#status`** — ★ 进度真相源。`outline → draft → archived` 驱动 Step 1 路由。归档时更新。
- **`settings/character-setting/<id>.yaml#state_history`** — ★ 角色状态唯一真相源。归档时追加，`state_history` 条目数必须等于该角色已归档章节数。
- **`archives/vol-{N}-ch-{M}-{slug}.md`** — ★ 正文唯一存放处。文件名有 `-draft` = 未归档，没有 = 已归档。
- **`volume-{N}.yaml#chapters_summary`** — 卷纲占位章纲，逐章讨论时详情写入 chapter.yaml。

**约定：**
- `chapters/` 只放章纲 yaml，不放正文
- `prompts/` 只放提示词 md，**纯生成产物**——可覆盖，不手动维护
- `archives/` 正文唯一存放处
- `settings/character-setting/` 每角色独立 yaml，追加写入不覆盖
- `volumes/` 卷纲 yaml，chapters_summary 只写占位章纲（逐章讨论时补充写入 chapter.yaml）

## 硬性自检协议（贯穿整个 Skill）

下面每个产出完成后，必须先自检 → 修复 → 再汇报/推进：

| 产出 | 生命周期 | 自检清单出处 |
|------|---------|-------------|
| 世界观 + 写作风格 + 题材设定 | 一次性（基本不改） | `references/world-setup-style.md` + `references/writing-style.md` + `references/genre-style.md` |
| 角色设定 | 基础一次性，后续可追加 | `references/character-setting-style.md` |
| 主线拆纲（story.md 故事主线 + 分卷规划） | 一次性（Phase 2 入口处） | `references/story-arc-style.md` |
| 卷纲（volume yaml） | 每卷一次 | `references/volume-checklist.md` |
| 章纲（chapter.yaml） | 每章一次 | `references/chapter-outline-checklist.md` |
| 提示词（prompt.md） | 每章一次 | `references/prompt-checklist.md` |
| 正文（archives/ 定稿） | 每章一次 | `references/chapter-body-checklist.md` + 深度评审（可选） |

**执行方式（按能力降级，优先用更隔离的方式）：**

1. **Agent Teams（最优）** — 开一个独立的 reviewer agent，给 ta "产出文件路径 + 对应清单 + 关键上下文"，逐项核查并严格汇报结论（哪几条 pass / 哪几条 fail + 证据 + 改写建议）
2. **subAgent（次优）** — 没有 Teams 能力但能开 subagent 就用 subagent 走同样流程
3. **自检（兜底）** — 当前没有上述能力，就自己严格逐项核查——不允许目测一遍就放行

**铁律：** 拿到结论后先按 fail 项把产出改完，再向用户汇报"做完了" + 自检结论 + 改了什么。直接拿原始结论汇报但不修复 = 违规。

## 各阶段文件读取指南

不同阶段必须读的文件不同。长会话中逐章循环重复 N 次，agent 容易遗忘约束——每次进入阶段必须先读"必读"文件再开始执行。

| 阶段 / 路由 | 必读（每次都看） | 一次性看完 / 按需查 |
|------------|-----------------|-------------------|
| **Phase 1 设定**（novel-setup） | `story.md`（项目索引，检查是否已初始化）+ `world-setting.yaml`（8 字段填写进度，引导逐项讨论）+ `scripts/templates/*` 全部 yaml 模板（字段结构参考） | `references/genre-example/index.md`（选类型时浏览 24 种 + 推荐）+ 自检：完成后逐项过 `references/world-setup-style.md`（世界观）+ `references/character-setting-style.md`（角色）+ `references/writing-style.md`（写作风格）+ `references/genre-style.md`（题材） |
| **Phase 2 卷纲**（novel-volume） | `story.md`（story_arc + 卷映射——总主线和分卷规划）+ `world-setting.yaml` core（geography / politics / rules——冲突空间来源）+ `writing-style.yaml`（role——叙事身份）+ `genre-setting.md`（pacing_rules——节奏基准） | `references/genre-example/` 对应类型的 `story_arc_templates`（卷结构参考）+ 角色 yaml（按需看动机）+ 自检：完成后逐项过 `references/volume-checklist.md` |
| **Phase 3.1 方向提案**（×N 次，每章一次） | 最新 `chapter.yaml#hooks`（pending / partial_advance 状态的钩子——读者期待来源）+ `volume-N.yaml#chapters_summary`（本章在卷内的定位）+ `genre-setting.md`（pacing_rules + satisfaction_types——节奏和爽点约束）+ 最近 1 章 `archives/` 结尾段（上一章结尾的情绪状态） | 所有角色 yaml（活跃角色的当前动机和冲突）+ `world-setting.yaml`（环境约束）+ 最近 3 章 `chapter.yaml#emotional_design`（情绪类型，避免连续同类型） |
| **Phase 3.2 章纲** | 方向提案确认结果 + `volume-N.yaml#chapters_summary`（本章占位章纲）+ 所有角色 yaml（性格 / 动机 / 关系——决策合理性来源） | hooks 相关的其他 `chapter.yaml`（跨章钩子追溯）+ 自检：完成后逐项过 `references/chapter-outline-checklist.md` |
| **Phase 3.3 自动提示词**（自动执行，×N 次） | **`writing-style.yaml` 四字段**（role / core_principles / possible_mistakes / depiction_techniques——缺一不可，缺失则 subagent 放飞）+ `references/genre-example/` 对应类型的 `prompt_segment`（题材特有叙事约束）+ 前文 `archives/` 最近 3 章（文风一致性）+ `world-setting.yaml`（场景 / 环境描述来源） | 角色 yaml（性格细节注入提示词 `character_voice`）+ 自检：组装后逐项过 `references/prompt-checklist.md` |
| **Phase 3.4 正文生成**（×N 次，被 3.3 调用） | `prompts/vol-N-ch-M-prompt.md` 单一入口——segment 拆分 + 逐段叙事指引 + 视角约束 + writing-style 注入 + genre prompt_segment / `agents/pipeline/exec-prose.md`（subagent 写作契约：输出格式 + 质量门禁 15 项 + 完工自检） | `archives/` 前文（文风参考，卡壳才翻——先按提示词自由写，不要抄袭前文句式） |
| **Phase 3.6 归档** | 当前 `chapter.yaml`（status→archived，hooks 操作写入）+ 各角色 yaml（追加 `state_history` + `emotional_arc`——每归档一章 state_history 条目数 +1） | 最近 3 章 `chapter.yaml`（滑动窗口审视参考）+ `prompts/volume-N-prompt.md`（追加本章一句话摘要） |
| **novel-review** | 目标正文 `archives/` + `writing-style.yaml`（评分基准：role / core_principles / possible_mistakes / depiction_techniques） | 角色 yaml（角色一致性校验）+ `world-setting.yaml`（设定一致性校验） |

**要点：**
- Phase 3.3 的 writing-style 四字段必须全部注入——role 定叙事身份，core_principles 定不可违背的写作信条，possible_mistakes 定 AI 易犯错误列表，depiction_techniques 定描写层次和手法。缺任何一个，subagent 都会在最关键的地方放飞。
- Phase 3.1 每个循环重读上一章的 hooks 和卷纲定位——方向提案的推理链来源不在子技能文件中，在当前项目的 chapter.yaml 和 archives/ 里。
- 正文字数目标、写作模型（writing_model）、情绪目标等执行参数从 `writing-style.yaml` 和 `chapter.yaml` 读取，不在 prompts/ 中重复定义——一处修改全局生效。

## The Process

### Step 1: 检测当前进度

读取项目根目录的 `story.md`。若不存在 → 项目未创建，Read `skills/setup/SKILL.md`。

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
| "评审""评价""review""检查这章""这章怎么样" | `novel-review`（独立检查） |
| "小说进度""第X卷进度" | 只读报告，不分发 |

### Step 3: 前置产出检查

根据目标路由检查前置文件：

| 目标 | 检查项 |
|------|--------|
| novel-volume | story.md story_arc 已定义（至少已完成主线拆纲）、settings/world-setting.yaml 非模板、writing-style.yaml 非模板 |
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
| novel-volume | 主线拆纲+卷纲规划 | `skills/outline/SKILL.md`（主线拆纲 + 卷纲部分） |
| novel-chapter-loop | 逐章写作循环 | `skills/chapter-loop/SKILL.md` |
| novel-review | 深度评审 | `skills/review/SKILL.md` |

子技能文件位于主技能安装目录的 `skills/` 下，即 `~/.claude/skills/awesome-novel/skills/{name}/SKILL.md`。

## Anti-Patterns

| 借口 | 现实 |
|------|------|
| "作者说写第一章，我直接生成所有文件" | 必须按 Phase 顺序推进 |
| "差不多就行，不用那么详细" | 缺 memo，subagent 不知道读者在等什么 |
| "视角转换跳过自动质量防护" | Agent 自动执行时仍需跑完整双轮净化和 AI 味自检 |
| "模板我看懂了，直接帮作者填好" | Agent 引导讨论，不代笔填 YAML |

## 模型门禁（MODEL-GATE）

```
深度推理阶段（Phase 1-3）→ 主会话必须使用 sonnet。
若不满足 → STOP，告知用户切换模型后再继续。不得在 haiku 下执行深度推理。
```

| Phase | 子技能 | 主会话模型 | 原因 |
|-------|--------|-----------|------|
| 1 | novel-setup | **sonnet（强制）** | 设定讨论——需要深度思考 |
| 2 | novel-volume | **sonnet（强制）** | 主线拆纲+卷纲规划——需要结构推理 |
| 3 | novel-chapter-loop | **sonnet（强制）** | 情节提案、章纲、视角转换——核心推理 |
| 3 | novel-chapter-loop（subagent 写作） | 从 `writing_model` 读取 | 正文生成，默认 haiku |
| — | novel-review | haiku 可 | 主 Agent 已持有全部上下文 |
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
| `references/genre-example/` | 类型案例（24 种预置类型，自包含文件） | Phase 2 设定阶段参考类型配置；Phase 3 提示词注入 prompt_segment |
