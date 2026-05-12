---
name: novel-chapter
description: 章纲设定——从卷纲拆出每章内容规划。触发："规划章节""章纲""这章写什么""拆章节"。章纲完成后自动路由到提示词生成。
---

# Novel Chapter — 章纲设定

> 流程：方向输入（含角色发声）→ 展开纲要点 → 禁止清单 → Memo 8段 → 情绪设计 → Hooks → 验收。章纲确认后自动进提示词生成。

## Overview

从卷纲的 chapters_summary 出发，逐章填充详细章纲。每章独立走完这个流程。

**When NOT to use:** 卷纲未完成（volume-N.md 不存在或无章节列表）、只是想查看已有章纲。

**Announce at start:** "我来引导你规划第{N}卷第{M}章的章纲。"

## 执行前提

| 检查项 | 操作 |
|--------|------|
| volume-N.md 存在且章节列表非空？ | 不存在 → STOP，先走 `novel-outline` |
| 本章 chapter.md 已存在且 status = draft？ | 是 → 章纲已确认，提示词已生成，直接路由到 `skills/prompt/SKILL.md` |
| 本章 chapter.md 已存在且 status = archived？ | 是 → 本章已完成，回主流程进入下一章 |

## 执行参数

- `{N}` = 当前卷号（从 volumes/ 目录取最大卷号）
- `{M}` = 当前章号（从 chapters/ 目录取当前卷最新未归档章号）
- `{slug}` = 章节标题的 slug 形式

## 章纲流程

Read `references/chapter-setting-style.md`，先执行"一、方向输入"：

1. **章级角色发声** — 读各活跃角色 yaml 的最新状态历史，生成每角色当前处境和动机。格式同卷级角色发声（`【处境】【未完成的事】【现在想做的事】`），范围收敛到上一章结束时
2. **收集四组输入** — 读者缺口（上章 emotional_hook）+ 角色状态（发声结果）+ 钩子盘点 + 卷纲定位
3. **合成 1-3 个方向** — 交叉输入推方向选项，展示给作者确认

详见指南。方向确认后，执行"二、从方向到纲要点"——用字数倒推法确定关键点数量，用三段锚点法填充每条关键点（感官/动作/判断），对话场景用对话变体（场景/对话/权力）。详见指南。

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

按以下格式展示，不要丢 YAML 原文：

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

**写入文件：** `chapters/vol-{N}-ch-{M}.md`，status → `outline`

**作者确认章纲后：**
- "继续" → 自动进入 `skills/prompt/SKILL.md` 生成提示词
- "调整" → 回到本章纲修改
