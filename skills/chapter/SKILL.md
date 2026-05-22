---
name: novel-chapter
description: 章纲设定——从卷纲拆出每章内容规划。触发："规划章节""章纲""这章写什么""拆章节"。章纲完成后自动路由到提示词生成。
---

# Novel Chapter — 章纲设定

> 流程：PreFlight（四 agent 并行）→ 作者确认规划草案 → 方向输入 → 展开纲要点 → 禁止清单 → Memo 8段 → 情绪设计 → Hooks → 验收。章纲确认后自动进提示词生成。

## Overview

从卷纲的 chapters_summary 出发，逐章填充详细章纲。每章独立走完这个流程。

**When NOT to use:** 卷纲未完成（volume-N.md 不存在或无章节列表）、只是想查看已有章纲。

**Announce at start:** "我来引导你规划第{N}卷第{M}章的章纲。"

## 工具契约

| 工具 | 用途 | 限制 |
|------|------|------|
| Read | 读卷纲 volume.md、角色设定文件、前章 chapter.md、references/chapter-setting-style.md | — |
| Write/Edit | 写 chapter.md（outline/memo/emotional_design/hooks）、更新 status → outline | 不改其他文件 |

## 错误恢复

| 失败场景 | 恢复策略 |
|---------|---------|
| 作者对方向提案一直不满意（3 次以上） | 缩小范围：作者指定一个方向，Agent 按此方向深入 |
| 角色文件缺失（角色发声阶段） | 跳过该角色的发声，标记"角色文件待建"，继续其他角色 |
| 验收 24 项部分不可检（如前章未归档） | 标记为 N/A，不影响其他项 |
| 作者说"差不多""你看着写"不通过 | 追问具体：哪条 key_point 不符预期？需要改什么？ |

## 执行前提

| 检查项 | 操作 |
|--------|------|
| volume-N.md 存在且章节列表非空？ | 不存在 → STOP，先走 `novel-outline` |
| 本章 chapter.md 已存在且 status = draft？ | 是 → 章纲已确认，告知作者"本章章纲已完成"，回主流程 |
| 本章 chapter.md 已存在且 status = archived？ | 是 → 本章已完成，回主流程进入下一章 |

## 执行参数

- `{N}` = 当前卷号（从 volumes/ 目录取最大卷号）
- `{M}` = 当前章号（从 chapters/ 目录取当前卷最新未归档章号）
- `{slug}` = 章节标题的 slug 形式

## PreFlight：四 agent 并行读取

规划新章前，必须先完成四份观察报告。**四 agent 并行读取，互不等待各自的输出。**

### 分发任务

主 agent 同时向四个 subagent 发送任务：

```
→ plot-agent      → skills/chapter/subagents/plot-agent.md
→ architecture-agent → skills/chapter/subagents/architecture-agent.md
→ emotion-agent  → skills/chapter/subagents/emotion-agent.md
→ reader-agent   → skills/chapter/subagents/reader-agent.md
```

### 1. 情节 agent（plot-agent）

职责：守住情节逻辑链——上章发生的事如何自然延续

读取：vol-{N}-ch-{M-1}.md（outline、key_points）、volume-{N}.md（chapters_summary）、相关角色文件（状态历史）

输出：`## 情节观察\n↳ 来源：vol-{N}-ch-{M-1}.md outline\n[上章关键情节]\n[本章情节如何衔接]`

### 2. 架构 agent（architecture-agent）

职责：守住钩子兑现路径——哪些旧钩子必须在这章处理

读取：所有 chapter.md 的 hooks 字段（汇总未兑现项）、story.md（story_arc）

输出：`## 架构观察\n↳ 来源：hooks 全局汇总\n[必须兑现的旧钩子]\n[本章应新增的钩子]\n[与主线的关系]`

### 3. 情绪 agent（emotion-agent）

职责：守住角色情绪弧线——角色此刻的心理状态

读取：vol-{N}-ch-{M-1}.md（emotional_design）、相关角色文件（状态历史）

输出：`## 情绪观察\n↳ 来源：vol-{N}-ch-{M-1}.md emotional_design\n[上章情绪弧线]\n[角色当前心理状态]\n[本章情绪走向建议]`

### 4. 读者 agent（reader-agent）

职责：守住读者期待——读者追到这章想知道什么

读取：vol-{N}-ch-{M-1}.md（emotional_hook）、所有未兑现钩子清单

输出：`## 读者观察\n↳ 来源：vol-{N}-ch-{M-1}.md emotional_hook\n[读者此刻最大的悬念]\n[读者期待的情感回报]\n[本章应给出的 micro_payoff 位置]`

### 主 agent 汇总 + 仲裁

收到四份报告后，主 agent **不自己读文件补充**，直接基于四份报告输出规划草案。

**仲裁规则：**

| 优先级 | 规则 | 说明 |
|--------|------|------|
| 1 | 架构 > 情节 | 钩子兑现是硬约束，情节逻辑不得违背钩子路径 |
| 2 | 架构 > 读者 | 必须兑现的钩子优先于读者期待的 micro_payoff |
| 3 | 情节 > 情绪 | 角色情绪不能与情节逻辑冲突——先有行动再有情绪 |
| 4 | 超出以上规则的冲突 | 标注【冲突】+ 两个 agent 的观点 → 提交作者仲裁 |

冲突报告格式：
```
【冲突】{agent A} vs {agent B}
- {agent A}：[内容]
- {agent B}：[内容]
→ 等待作者裁定
```

### 规划草案输出格式

```
## 规划草案

### 本章定位
[一句话，基于四份报告综合]

### 情节方向
[基于情节 agent 报告]

### 必须兑现的钩子
[基于架构 agent 报告]

### 情绪走向
[基于情绪 agent 报告]

### 读者期待回应
[基于读者 agent 报告]
```

展示给作者确认后，才进入"一、方向输入"阶段。

---

## 执行顺序

```
PreFlight（四 agent 并行）→ 作者确认规划草案 → 方向输入 → 展开纲要点 → ...
```

**没有四份报告，规划草案不能输出。**

## 章纲流程

规划草案经作者确认后，进入章纲细化阶段。

Read `references/chapter-setting-style.md`，按以下步骤执行：

### a. 展开纲要点（Agent 填充，作者确认）

展开 8-12 条 key_points，每条 2-3 句锚点描述 + 功能类型标记（`[推进剧情]`/`[造悬念]`/`[过渡]`），有对话的加 `[对话]`。写一句 summary，列出 characters/location/time，确认 narrative_pov。

**STOP：作者确认 outline。**

### a2. 禁止清单

必须询问："本章有没有明确禁止出现的场景、元素或情节？" 记录到 memo.prohibitions。作者说"没有"也要确认一次。

### b. Chapter Memo（8 段，Agent 填充，一次展示确认）

从方向纲要自动填充，不逐段讨论。填充后展示完整 memo 供作者确认。

- current_task：要达成本章改变必须完成的具体推进动作
- reader_expectation：读者情绪状态 + 本章策略 + 具体说明（详见指南三子字段）
- payoff_plan：三列表——must_resolve（旧钩子了结）/ must_hold（不能碰的悬念）/ partial_advance（推进不收束+新钩子）
- downtime_functions：过渡场景的功能映射，每段 [场景] → [功能]
- key_choices：角色选择 + 为什么 + 符合人设 + 读者感受
- knowledge_state：每个出场角色知道什么/不知道什么 + 信息差 + 对话标记
- required_changes：1-3 条，每条标注改变类型 + "从什么变成什么"
- prohibitions：从 a2 来

### c. Emotional Design

primary_mood、mood_progression、intensity_peak、emotional_hook、intensity_level、micro_payoffs

**micro_payoffs（读者获得）：** 每章至少 1 个，类型：info/relationship/emotion/clue/ability/resource/recognition。放在前段/中段（不和章末情绪钩子抢位置）。过渡章也必须至少 1 个。

### d. Hooks 操作

在 chapter.md 中写入本章的钩子操作（埋/推进/收束）。**不读写全局 hooks.md——真相源仅在各 chapter.md 的 hooks 字段。**

### e. 验收（章纲完成后强制执行，全部通过才进提示词生成）

详见 `references/chapter-setting-style.md#做完之后验收流程`。以下为 SOP 摘要：

**第 1 步：给作者看 structured 反馈**

按以下格式展示，不要丢原文：

```
📋 第{N}章 章纲反馈

本章定位：{一句话}
主要内容：{2-3 句}

关键场景：
- {title}（角色：{人物列表}）
- ...

冲突进展：{推进了什么}
字数目标：{N} 字
```

作者必须明确说"对"才算合格。"差不多""你看着写"不算通过。

**第 2 步：检查清单自检**

24 项详见指南 checklist。以下为高频必检项：

- [ ] 字数目标已确认（4000+）
- [ ] 段落分布已确认（推进/过渡/埋伏笔各几段）
- [ ] 每条 key_point 对应一个可写场景，含冲突事件
- [ ] 旧钩子兑现/新钩子埋下已记录
- [ ] 硬约束（prohibitions）每条可验证
- [ ] 情绪走向至少三个节点（A→B→C）

**第 3 步：快速嗅探**

遮住章纲能不能说出：
- 分多少条、每条写什么场景
- 每个角色知道什么、不知道什么
- 兑现了哪些旧钩子、新埋了什么钩子

**第 4 步：AI 味自检**

| # | 检测项 | 扫描字段 | 命中模式 |
|---|--------|---------|---------|
| 1 | 上帝视角概述 | outline、memo.current_task | "本章讲述了""主角经历了""本章将展示" |
| 2 | 抽象心理总结 | memo.reader_expectation、memo.key_choices | "他感到""他意识到""他内心挣扎" |
| 3 | 分析性结论 | memo.reader_expectation、memo.required_changes | "这表明""这意味着""这标志着关系转折" |
| 4 | 文学评论腔 | outline、memo.current_task | "通过X展现了Y""完成角色弧光转折" |
| 5 | "不是而是"句式 | 所有字段 | "不是X，而是Y" |
| 6 | 抽象标签 | memo.current_task、memo.required_changes | "关系递进""冲突升级"——应写具体事件 |

**作者确认章纲后：**
- 写入 `chapters/vol-{N}-ch-{M}.md`，status → `outline`

## 下一步

**状态汇报 + 自动路由：**
- ✅ 章纲：`chapters/vol-{N}-ch-{M}.md` → `status: outline`
- → 主流程检测到 `status=outline` + 无 prompt 文件，**分发到提示词生成**（`skills/prompt/SKILL.md`）
