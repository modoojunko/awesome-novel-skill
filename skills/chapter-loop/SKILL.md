---
name: novel-chapter-loop
description: 逐章写作循环——从章纲到正文归档的完整闭环。触发："写正文""写第X章""继续写""下一章""继续""规划章节""章纲"。
---

# Novel Chapter Loop — 逐章写作循环

> 摘要：章纲 → 自动提示词 → 写正文 → 质量门禁 → 审阅 → 归档。每章一个闭环，第 1 章强制锚点。

## Overview

一卷的每章独立走完这个循环：卷纲给的 chapters_summary 作为方向 → 确认章纲 → 审阅正文 → 归档。中间步骤全自动。

**When NOT to use:** 卷纲未完成（volume-N.md 不存在或无 chapters_summary）。

**Announce at start:** "我来引导你完成第{N}卷第{M}章的写作。"

---

## 执行前提

| 检查项 | 操作 |
|--------|------|
| volume-N.md 存在且 chapters_summary 非空？ | 不存在 → STOP，先走 `novel-volume` |
| 本章 chapter.md 已存在且 status = draft？ | 是 → 提示词已生成但正文未归档，跳到 Step 3（写正文） |
| 本章 chapter.md 已存在且 status = archived？ | 是 → 本章已完成，自动推进到下一章 |

## 执行参数

- `{N}` = 当前卷号（从 volumes/ 目录取最大卷号）
- `{M}` = 当前章号（从 chapters/ 目录取当前卷最新未归档章号）
- `{slug}` = 章节标题的 slug 形式

## Step 1: 章纲

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

**写入文件：** `chapters/vol-{N}-ch-{M}.md`

**STOP：作者确认章纲。** 确认后自动进入 Step 2。

---

## Step 2: 自动生成提示词

章纲确认后自动执行，无 STOP：

1. 拆 segment（不持久化到 YAML）
2. 视角转换 → 双轮净化（结构层 + 词句层）
3. 读 writing-style.md / references/genre-example / world-setting / archives
4. 组装 `prompts/vol-{N}-ch-{M}-prompt.md`
5. 文件头部写入标记：`# 自动生成 — 修改章纲后重新生成覆盖。手动编辑不持久。`
6. AI 味自检 → 命中自动修复 → 二次扫描确认
7. chapter.md status → `draft`
8. 更新 `.agent/status.md`：current_phase = chapter-loop, current_chapter = {M}, project_status = writing

**汇报结果：**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  提示词已自动生成
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  章节: 第{N}卷第{M}章《{title}》
  segment: {N} 段
  AI 味检测: {通过/修复}情况
  提示词文件: prompts/vol-{N}-ch-{M}-prompt.md

  直接写正文，还是看一眼提示词？
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

"写正文" → Step 3
"看一眼" → 展示提示词内容
"我自己调" → 手动编辑 prompt 文件（标注已手动调整标记，重生成时不会覆盖）

---

## Step 3: 写正文 + 质量门禁

### 写正文

Read `agents/pipeline/exec-prose.md`，注入写作参数后调用写作 subagent：
- 使用 `writing_model` 字段指定模型（默认 haiku）
- 写入 `archives/vol-{N}-ch-{M}-{slug}.draft.md`

### 质量门禁（15 项硬性检查）

逐项执行。任意一项触发 → **不展示正文**，报告问题及触发项编号。

| # | 检查项 | 不通过处理 |
|---|--------|-----------|
| 1 | 字数不达标 | 报告实际字数 vs 要求 |
| 2 | 上帝视角摘要 | 摘出典型句 |
| 3 | 违反核心约束 | 指出违规条款和位置 |
| 4 | 夹带非正文内容 | 指引导语、解释、文末总结 |
| 5 | AI疲劳词 | 扫描 fatigue_words，报告风险等级 |
| 6 | AI句式违规 | 连续同结构开头、列表式叙述 |
| 7 | 结构性句式癖好 | 超阈值报告 |
| 8 | 章尾情绪缺口 | 无有效钩子 → "缺钩子" |
| 9 | 情绪兑现 | 旧缺口兑现 + 新缺口制造 |
| 10 | 跨章情绪单调 | 最近 3-5 章情绪连续相同？ |
| 11 | 微兑现缺失 | 至少一处"有收获"段落 |
| 12 | 安全着陆 | 完美解决冲突 → 无继续动力 |
| 13 | 物品/状态一致性 | 物品消耗后仍出现？ |
| 14 | 句式单调检测 | 连续 4 句相同开头 |
| 15 | 身体反应模板化 | 高密度复用同一反应 |

### 长篇小说附加检查（16-18，项目存在 foreshadowing.md 等追踪文件时执行）

| # | 检查项 | 不通过处理 |
|---|--------|-----------|
| 16 | 时间线冲突 | 对照 timeline.md，story_date 与前章间隔不合理或矛盾 |
| 17 | 伏笔遗漏 | 对照 foreshadowing.md，前卷活跃伏笔本章应触及但未触及 |
| 18 | 设定版本对齐 | 新引入的设定元素与 setting-change-log.md 已有记录冲突 |

全部通过 → 执行深度评审（主 Agent 直接执行 `novel-review`）

---

## Step 4: 作者审阅

```
━━━━━━━━━━━━━━━━━━━━━━━━
  第{N}卷第{M}章正文：《{title}》
━━━━━━━━━━━━━━━━━━━━━━━━
[正文全文]

━━━━━━━━━━━━━━━━━━━━━━━━
  深度评审报告
━━━━━━━━━━━━━━━━━━━━━━━━
[novel-review 评审报告全文]
```

**作者操作：**
- "满意" → 归档（执行 Step 5）
- "修改第X段" → 指定修改意见，主 Agent 直接编辑
- "重写全章" → 回 Step 3

---

## Step 5: 归档

### 文件操作
1. `archives/vol-{N}-ch-{M}-{slug}.draft.md` → `archives/vol-{N}-ch-{M}-{slug}.md`
2. chapter.md status → `archived`

### 状态更新
3. 分析角色变化，追加 `状态历史` 到角色 yaml
4. 追记 `情绪弧线`
5. **更新 hooks**：从当前 chapter.md 读取 hooks 操作，追加到各角色 yaml。**不维护全局 hooks.md。**

### 长篇小说追踪文件（项目 `settings/` 下存在对应文件时执行）
6. **timeline.md 追加**：读 `settings/timeline.md`，提取本章 `outline.story_date` 和核心事件，追加一行到 timeline 表格
7. **foreshadowing.md 重新生成**：扫描 `chapters/` 下各 chapter.md 的 hooks 字段，重新生成 `settings/foreshadowing.md` 的三张汇总表（活跃/已收束/废弃伏笔）
8. **setting-change-log.md 检查**：比对本章正文引入的新设定元素与初始设定。有显着偏离 → 追加一行到 `settings/setting-change-log.md`

### 动态报告（不落盘）
9. 运行情节推进停滞检测
10. **滑动窗口审视**（动态生成）：

```
## 滑动窗口审视（第 {M} 章归档后自动生成）

最近 3 章：第 {M-2}-{M} 章
节奏评估：{分析结论}
钩子状态：{活跃钩子列表}
优先级建议：{建议}

作者 actions：
- "继续下一章" → 进入 Step 6
- "先停" → 结束
```

### 卷完成检测
11. 读 `chapters/` 目录，检查当前卷所有章节是否全部 archived：
   - 未全部完成 → 问"下一章继续？"
   - 全部完成 → 卷完成报告 + "下一卷 / 回顾 / 修改"

### 状态持久化
12. 更新 `.agent/status.md`：
    - current_chapter → {M+1}（如本卷还有下章）或保持 {M}（卷完成时）
    - last_volume_completed → true（卷全部归档时）
    - project_status → writing（如还有章节）或 paused（作者选暂停时）

---

## 第 1 章锚点

第一卷第一章必须走完整流程（章纲→提示词→写→审阅→归档），不可跳过任何步骤。

---

## Step 6: 下一章决策

归档后自动检测：
- 本卷还有未归档章节？→ `下一章继续吗？（Y/N）`
- 本卷全部完成 → 卷完成报告 + 选项
  - "规划下一卷" → 回到 SKILL.md 路由到 novel-volume
  - "回顾整卷" → Read `skills/review/SKILL.md` 做整卷评审
  - "修改某章" → 指定章节修改

### 跨卷检查（规划下一卷前执行）

项目存在 `settings/foreshadowing.md` 等长篇小说追踪文件时，在进入 `novel-volume` 前执行三项预检：

1. **伏笔完整性**：读 `settings/foreshadowing.md` 活跃伏笔表，确认前卷未收束钩子已知悉并计划在新卷处理。遗漏活跃钩子 → 报告
2. **时间线衔接**：读 `settings/timeline.md`，确认两卷间 `story_date` 间隔合理（无跳跃断裂或时间倒流）。矛盾 → 报告
3. **角色状态连续性**：读角色 yaml 和 `settings/setting-change-log.md`，确认前卷结束时角色状态已记录且与新卷起点一致。不一致 → 报告

三项预检结果汇总给作者后，再进入卷规划。
