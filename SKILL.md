---
name: awesome-novel
description: 和 AI 协作写小说的工作流系统。流程：一次设定→规划卷纲→逐章写作循环（章纲→提示词→验收→正文→验收→评审→归档→下一章）。适用场景：从零写新小说、导入已有小说。
---

# Novel — 小说创作工作流

和 AI 一起写小说。**一次设定**世界观/角色/写作风格 → **主线拆纲+卷纲展开** → **逐章写作循环**（章纲→提示词→提示词验收→正文→正文验收→评审→归档→下一章）

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

- **`chapters/vol-{N}-ch-{M}.md#status`** — ★ 进度标记。`outline → draft → archived` 驱动 Step 1 判断该做什么。归档时更新。
- **`settings/character-setting/<id>.md` → 状态历史** — ★ 角色状态的唯一记录。归档时追加，状态历史条目数必须等于该角色已归档章节数。
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

| 产出 | 时效 | 自检清单出处 |
|------|---------|-------------|
| 世界观 | 基础一次性，后续可追加 | `references/world-setup-style.md` |
| 写作风格 + 题材设定 | 一次性（基本不改） | `references/writing-style.md` + `references/genre-style.md` |
| 角色设定 | 基础一次性，后续可追加 | `references/character-setting-style.md` |
| 主线拆纲（story.md 故事主线 + 分卷规划） | 一次性（Phase 2 入口处） | `references/story-arc-style.md` |
| 卷纲（volume-N.md） | 每卷一次 | `references/volume-setting-style.md` |
| 章纲（chapter.md） | 每章一次 | `references/chapter-setting-style.md` |
| 提示词（prompt.md） | 每章一次 | `references/prompt-setting-style.md` |
| 正文（archives/ 草稿） | 每章一次 | `references/chapter-quality-checklist.md`（正文验收，主流程独立执行） |

**自检方式（推荐用独立助手完成）：**

1. **独立检查助手（推荐）** — 开一个专门的检查助手，告诉它"产出文件路径 + 对应清单 + 关键信息"，逐项核查后报告结论（哪几条 pass / 哪几条 fail + 证据 + 修改建议）
2. **辅助助手** — 没有独立助手条件时，用辅助助手走同样流程
3. **自己检查（兜底）** — 上面两种都不行时，自己严格逐项核查——不允许目测一遍就放行

**铁律：** 拿到结论后先按不合格项把产出改完，再向用户汇报"做完了" + 自检结论 + 改了什么。直接拿原始结论汇报但不修复 = 违规。

## 各阶段文件读取指南

每个子步骤按"写什么文件 → 读什么参考 → 可选的参考阅读"来准备。读完一份，再看下一份。

| 子步骤 | 写什么文件 | 必读的参考 | 参考阅读 |
|--------|---------|--------------|---------|
| **1.1 新建项目** | 项目骨架 + `story.md` | `scripts/init.py`（创建骨架） | — |
| **1.2 题材选择+风格** | `settings/genre-setting.md`<br>`settings/writing-style.md`（预填） | `references/genre-style.md`（选题指南+验收） | `references/genre-example/` 对应类型（配置参考） |
| **1.3 世界观** | `settings/world-setting.md` | `references/world-setup-style.md`（引导讨论+自检） | — |
| **1.4 角色** | `settings/character-setting/<id>.md` | 已有角色文件（追加时不覆盖）<br>`references/character-setting-style.md`（认知6层+自检） | — |
| **2.0 主线拆纲** | `story.md#story_arc`（主线+分卷） | `references/story-arc-style.md`（从结局倒推法） | `settings/world-setting.md` core（冲突空间参考）<br>角色文件（按需看动机） |
| **2.1 卷纲** | `volumes/volume-{N}.md`（章节列表） | `references/volume-setting-style.md`（指南+自检） | — |
| **3.1 章纲** | `chapters/vol-{N}-ch-{M}.md` | `volumes/volume-{N}.md#chapters_summary`（卷纲给的本章方向）<br>`references/chapter-setting-style.md`（指南+自检） | — |
| **3.2 提示词** | `prompts/vol-{N}-ch-{M}-prompt.md` | `references/prompt-setting-style.md`（提示词指南+模板） | — |
| **3.2a 提示词验收**（主流程独立执行） | `prompts/vol-{N}-ch-{M}-prompt.md`（检查对象） | `references/prompt-setting-style.md` Section 三（验收标准） | — |
| **3.3 正文生成** | `archives/vol-{N}-ch-{M}-*.draft.md` | `prompts/vol-{N}-ch-{M}-prompt.md`（单一入口） | `skills/write/SKILL.md`（SOP） |
| **3.3a 正文验收**（主流程独立执行） | `archives/vol-{N}-ch-{M}-*.draft.md`（检查对象） | `references/chapter-quality-checklist.md`（验收标准） | — |
| **3.4 深度评审**（可选） | 诊断报告（内存） | `skills/review/SKILL.md` | — |
| **3.5 归档** | `archives/vol-{N}-ch-{M}-*.md`（去 draft）<br>`chapters/vol-{N}-ch-{M}.md`（status→archived）<br>角色状态追加 + `status.md` 更新 | 各角色文件（追加状态历史+情绪弧线） | 最近 3 章 `chapters/`（回顾最近章节） |

## 工作机制：状态驱动循环

主 SKILL.md 和子 skill 之间没有显式"调用"。整个系统是一个**状态驱动循环**：

```
Step 1（检测状态）→ 匹配路由 → Read 子 skill → 子 skill 改状态 → 回到 Step 1（重新检测）
```

**通信方式：** 不传递消息或参数。主 skill 写 `chapter.md#status` + `.agent/status.md`，子 skill 读这些文件来知道"当前在做什么阶段"。

- 主 skill Step 1 检测 `chapters/` 下的状态 → 匹配到对应子 skill
- 主 skill Step 2.3 读子 skill 的 SKILL.md，**Agent 直接执行里面的步骤**
- 子 skill 修改 `chapter.md#status` 和产出文件，末尾写"回到主流程"
- Agent 读"回到主流程"后，**重新从 Step 1 开始**，检测到新状态后再路由到下一步

**分发判断方式：** Step 1 的决策表（见下）是唯一的路由入口——根据 `status` + 文件存在性做二元判断。子 skill 不自作主张跳转到其他子 skill。

## SOLO Mode（单机模式）

当作者明确说"solo""单机""你全权写"或"你当作者"时进入此模式。SOLO 模式下 Agent 同时承担作者和写作者角色，所有创作决策自主做出，流程压缩为单向推进。

### 触发条件

作者说出触发词即进入 SOLO 模式，之后所有子技能继承此模式。一次会话内持续生效，作者说"退出 solo""回来确认"时退出。

### 与"全部授权"的区别

- **全部授权**：流程节点仍在，STOP 还在，只是用户授权 Agent 代按确认。子技能仍 dispatch sub-agent，正文仍走提示词→sub-agent 写→验收链路。
- **SOLO 模式**：流程简化。无 STOP 点，无用户确认步骤，无 sub-agent 分发。Agent 一人完成全部创作和写作。

### 行为变更

| 流程节点 | 正常模式 | SOLO 模式 |
|---------|---------|-----------|
| 设定讨论（世界观/角色/风格） | 引导讨论，逐项确认 | Agent 直接撰写，不自检不展示 |
| 题材选择 | 展示选项等作者选 | Agent 根据项目信息自行选择 |
| 方向提案 | 展示 3-4 个方向等作者选 | Agent 直接选定一个方向深入 |
| 章纲确认 | **STOP** 展示等作者确认 | 直接写入文件，不展示 |
| 视角转换确认 | **STOP** 展示等作者确认 | 直接执行双轮净化，不展示 |
| 提示词生成 | 自动生成后问"看一眼？" | 自动生成，不询问 |
| 正文写作 | dispatch 到 sub-agent（writing_model） | 主 Agent 直接撰写 |
| 正文验收（15项质量门禁） | 逐项检查，汇报结果 | 快速自检，有问题自行修复 |
| 深度评审 | 展示报告等作者决定"满意/修改" | 快速自检，通过即归档 |
| 归档 | 展示滑动窗口，问"下一章？" | 自动归档，自动推进到下一章 |
| 卷完成 | 展示完成报告和选项 | 自动规划下一卷或询问"继续？" |

### 保留的约束

SOLO 模式只跳过"用户确认"环节，以下约束**仍然强制执行**：

1. **Phase 顺序不可跳过**——仍须按 设定→卷纲→章纲→提示词→正文→归档 推进。跳 Phase 等于让 Agent 在没有上下文的情况下瞎写。
2. **产出文件完整**——每个 Phase 的产出文件必须写入磁盘（story.md / world-setting.md / volume-N.md / chapter.md / prompt.md / archives）。SOLO 不意味着不留记录。
3. **质量门禁**——15 项正文检查 + AI 味自检仍需执行，只是不自检不展示，自检修复后直接推进。
4. **角色状态跟踪**——归档时仍须更新角色状态历史和情绪弧线，hooks 仍须维护。
5. **模型门禁**——Phase 1-3 仍须 sonnet，正文写作可降级但不强制执行。

### 状态驱动循环兼容

SOLO 模式不改变"状态驱动循环"机制——仍通过 `chapter.md#status` + `.agent/status.md` 驱动 Step 1 检测和路由。区别在于 Step 1 检测到状态后不自检不问用户，直接执行下一步。

### 跨章节上下文管理

SOLO 模式下每完成一章（正文验收通过 + 归档完毕），必须在 `.agent/status.md` 中写入当前进度后，执行上下文重置：

**每完成一章 → 告诉作者 `输入 /new 继续下一章`。**

这样做的原因：
1. **正文写作消耗大量上下文**——一章 4000+ 字进入对话后，下一章的推理空间被严重压缩
2. **状态驱动循环天然支持跨会话**——`chapter.md#status` + `.agent/status.md` 是持久状态，新会话读这些文件就能准确知道"当前章节写完了，该走下一步"
3. **角色状态已落盘**——归档时已追加角色状态历史，新会话通过读角色文件即可恢复上下文，无需保留前章对话

**新会话恢复流程：**
1. 用户在新会话中输入项目路径（`cd {project}`）
2. 告诉 Agent "继续写小说" 或触发 awesome-novel 技能
3. 主 SKILL.md Step 1 读 `.agent/status.md` → 检测到上一章已 archived → 自动推进到下一章
4. Agent 读 `volume-{N}.md` 获取本章方向 + 角色文件获取最新状态 → 从章纲开始新一章循环

**约束：** 归档不完整（角色状态未更新 / hooks 未维护 / 草稿未去 draft）时禁止触发 `/new`——必须在上下文重置前保证磁盘状态完整。

## 主 Agent 运作流程

### Step 1: 检测当前进度

先读 `story.md`：

1. **`story.md` 不存在，但 `story.yaml` 存在** → 旧版 v2.x 项目 → 分发到 `skills/migrate/SKILL.md` 执行迁移
2. **`story.md` 存在** → 读 `skill_version` 字段。低于当前版本（如 < 3.0）→ 需要升级迁移 → 分发到 `skills/migrate/SKILL.md`
3. **`story.md` 存在且版本匹配** → 正常流程，执行 `python detect_phase.py --write` 检测实际状态并写入 `.agent/status.md`（自动扫描 volumes/、chapters/、archives/ 下的文件状态，与缓存交叉验证）。然后读 `.agent/status.md` 快速定位。如果 detect_phase.py 不可用 → 回退手动扫描：读 `chapters/` 下最大章号的 `status` 字段。
4. **两者都不存在** → 新项目 → Read `skills/setup/SKILL.md`

**版本检测命令：**
```bash
# 旧版格式检测
test -f story.yaml && test ! -f story.md && echo "v2x"
# skill_version 检测
grep -E "技能版本.*3\.0" story.md && echo "version_ok"
```

正常流程信号表：

| 信号 | 下一步 |
|------|--------|
| 无 volumes/ 或无 volume md | → `novel-setup`（先完成设定和卷纲）|
| settings/world-setting.md 字段大量为空 | → `novel-setup`（设定未完成）|
| 最新 chapter.md status = `outline`，无 prompt 文件 | → 分发 `skills/prompt/SKILL.md` 生成提示词 |
| 最新 chapter.md status = `outline`，prompt 文件已存在 | → 分发 `skills/prompt-verify/SKILL.md` 做提示词验收。通过 → 更新 status = `draft`。不通过 → 返回 `skills/prompt/SKILL.md` 修改 |
| 最新 chapter.md status = `draft`，`archives/` 无本章草稿 | → 分发 `skills/write/SKILL.md` 写正文 |
| 最新 chapter.md status = `draft`，`archives/` 有本章草稿 | → 分发 `skills/body-verify/SKILL.md` 做正文验收。通过后，问作者"进入归档还是先做深度评审？" |
| 最新 chapter.md status = `archived` | 本卷还有未归档章？→ 问"下一章继续？"。全部归档 → 卷完成报告 + 选项 |
| 无任何 chapter.md | → 卷纲已定但尚未开始写 → 问"开始写第一章？" |

**章状态：** `outline`（章纲已定）→ `draft`（正写作/修改）→ `archived`（已归档）

### Step 2: 分发

匹配用户意图 → 前置检查 → 选择对应模块。

**1）匹配用户意图**

| 用户说 | 去向 |
|--------|------|
| "创建项目""写小说""导入""讨论设定""设计角色""世界观""写作风格" | Phase 1 `novel-setup` |
| "规划卷纲""定卷""下一卷""故事线" | Phase 2 `novel-volume` |
| "规划章节""章纲""这章写什么" | → `novel-chapter`（章纲设定） |
| "提示词""生成本章提示词" | 检测章 status：`outline` 且无 prompt → `novel-prompt` / 已有 → 提示词验收 |
| "写正文""写第X章""继续写" | 检测章 status + archives 文件 → Step 1 自动分发 |
| "评审""review""检查这章""这章怎么样" | `novel-review`（10 维深度诊断） |
| "归档""存档" | 检测 archives 有草稿 → `novel-archive` |
| "小说进度""第X卷进度" | 只读报告，不分发 |

**2）前置产出检查**

| 要去哪个模块 | 检查项 |
|------|--------|
| novel-volume | story.md story_arc 已定义、world-setting.md + writing-style.md 非模板 |
| novel-chapter | volume-{N}.md 存在且 chapters_summary 非空 |
| novel-prompt | chapter.md status = outline、memo + emotional_design 完整 |
| novel-write | chapter.md status = draft、prompt 文件存在 |
| novel-review | archives/ 有正文文件 |
| novel-archive | archives/ 有草稿文件、正文验收已通过 |

缺失 → **STOP**，告知作者先补前置产出。

**3）分配并执行**

前置检查通过后，Read 对应子技能的 SKILL.md，按其中的流程执行。子技能执行完后**自动回到 Step 1 重新检测进度**。

| 模块 | 读取并执行 |
|------|-----------|
| novel-migrate | `skills/migrate/SKILL.md` — 旧版项目迁移到 3.0 格式 |
| novel-setup | `skills/setup/SKILL.md` — 项目初始化 + 设定 |
| novel-volume | `skills/outline/SKILL.md` — 主线拆纲 + 卷纲 |
| novel-chapter | `skills/chapter/SKILL.md` — 章纲设定 |
| novel-prompt | `skills/prompt/SKILL.md` — 提示词生成 |
| novel-write | `skills/write/SKILL.md` — 正文生成 |
| novel-review | `skills/review/SKILL.md` — 深度评审 |
| novel-archive | `skills/archive/SKILL.md` — 归档 |

