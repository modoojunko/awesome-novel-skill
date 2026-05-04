---
name: novel-outline
description: 卷纲和章纲规划。Phase 3。当设定完成后需要规划故事结构时使用——卷纲、逐章章纲（含 memo 读者情绪设计和 emotional_design）。触发："规划章节""讨论章纲""分卷""第X章怎么写""故事线""卷纲"。即使只说"下一章写什么"也应先加载本技能确认章纲是否完整。
---

# Novel Outline — 卷纲与章纲

## Overview

引导作者拆分故事线、讨论卷纲、逐章设计章纲（含 memo 读者情绪设计和 emotional_design）。讨论期待值管理、章纲节奏、开篇设计时，参考 `best-practices.md` 中的模式和案例。

**When NOT to use:** 设定未完成（world-setting 为空）、章纲已完成（status = draft 或 archived）、只是想查看已有章纲。

**Announce at start:** "我来引导你规划章节。先确认卷纲，再逐章讨论。"

讨论章纲时参考 `best-practices.md` 中的模式和案例引导作者。

## HARD-GATE

```
章纲 memo（7 段）和 emotional_design 逐章讨论，不可跳过。
memo 缺失 → Phase 4 subagent 不知道"读者此刻在等什么"。
```

## 进入门禁

| 检查项 | 操作 |
|--------|------|
| author-intent.md | 核心主题已有 / 仍是模板？ |
| current-focus.md | 1-3章聚焦已有 / 仍是模板？ |
| 任一仍是模板 | **STOP** — 先问作者填写 |

## 流程（以卷 1 为例）

### 卷纲
1. 创建 `volumes/volume-1.yaml`，写入卷标题和卷概要
2. 讨论卷纲：核心冲突、主要事件、角色弧光走向
3. 将章节摘要列表写入 chapters_summary

### 生成卷提示词
读取 volume-N.yaml + story.yaml → 组装 `prompts/volume-{N}-prompt.md`：
- 本卷核心冲突与主线
- 章节列表（标题 + 概要，未写留空）
- "已完成章节摘要"区（初始为空，Phase 6 归档时追加）

### 逐章章纲（每章必做）

#### a. Outline
讨论剧情要点 → 填入 outline 字段（含 narrative_pov）。若作者未指定视角，沿用上一章设定。

#### a2. 禁止清单
**必须询问：** "本章有没有明确禁止出现的场景、元素或情节？" 记录到 memo.prohibitions。作者说"没有"也要确认一次。

#### b. Chapter Memo（7 段）
填写每段时触发以下诊断（参考 best-practices.md）：
- current_task：本章必须完成的具体动作
- reader_expectation：**诊断：** "这一章读者最想知道答案的问题是什么？你打算回答多少？留多少？"（参考「期待值管理」）
- payoff_plan：该兑现 / 暂不掀的伏笔
- downtime_functions：**诊断：** "这个平淡段落的'前因'可以是什么？如果让剧情一层层变得更糟，第一层是什么？"（参考「流水账修复」）
- key_choices：关键抉择三连问
- required_changes：章尾必须改变的 1-3 条
- prohibitions：硬约束红线

#### c. Emotional Design
primary_mood、mood_progression、intensity_peak、emotional_hook、intensity_level
**诊断：** "这一章结尾，读者最担心什么？最有好奇心的问题是什么？"（参考「钩子设计」和「期待值管理」）

#### d. 钩子操作
upsert（埋新）→ 归档时从正文提取 seed_text / mention（推进）/ resolve（收束）→ Phase 4 视角转换时注入 seed_text
**诊断（参考「四种开头钩」）：** "本章开头的钩子是什么类型——硬悬疑、思路式、人设式还是目标式？"

#### e. 更新 hooks.yaml

#### f. 微兑现设计
从以下 7 种中选择 ≥1 种，过渡章也至少 1 个。无微兑现 → 警告作者：
- **信息兑现**：读者知道了之前不知道的事（新线索/新信息）
- **关系兑现**：角色间的距离发生了变化（推进/接触）
- **情绪兑现**：读者感到爽、暖、释然或被触动
- **线索兑现**：之前的伏笔在本章有进展
- **能力兑现**：角色变强或获得新工具
- **资源兑现**：角色得到物品/资源
- **认可兑现**：角色被他人承认或尊重

### 填写 current-focus.md
填入 1-3 章聚焦：当前优先级、需推进支线、需提及钩子、节奏意图、限制约束。

### AI味自检（章纲完成后强制执行）

章纲确认前，扫描以下字段的 AI 味。命中即修，不把分析腔留给 Phase 4。

#### 检测清单

| # | 检测项 | 扫描字段 | 命中模式 |
|---|--------|---------|---------|
| 1 | 上帝视角概述 | outline、memo.current_task | "本章讲述了""主角经历了""本章将展示""故事发展到" |
| 2 | 抽象心理总结 | outline、memo.reader_expectation、memo.key_choices | "他感到""他意识到""他内心挣扎""经历了复杂的心理变化" |
| 3 | 分析性结论 | memo.reader_expectation、memo.required_changes | "这表明""这意味着""整件事的性质""这标志着关系转折" |
| 4 | 文学评论腔 | outline、memo.current_task | "通过X展现了Y""完成角色弧光转折""实现情感升华" |
| 5 | "不是而是"句式 | 所有字段 | "不是X，而是Y""不是…是…"——章纲阶段就禁止此句式 |
| 6 | 抽象标签替代具体事件 | memo.current_task、memo.required_changes | "关系递进""情感爆发""冲突升级"——应写具体事件，不写类型标签 |

#### 输出

```
## 章纲 AI 味自检

| 字段 | 命中项 | 处理 |
|------|--------|------|
| outline | 通过 | — |
| memo.current_task | 通过 | — |
| memo.reader_expectation | #3 分析性结论："这表明凶手早有预谋" | 已改为"凶手的准备比警方早三天——这一点在本章末尾会浮现" |
| memo.required_changes | #6 抽象标签 | 已改为具体事件 |

通过率：5/7 字段一轮通过。2 字段经修复后通过。
```

全部通过后，**STOP：作者确认。**

## 下一步

完成后引导进入 Phase 4。当作者说"生成提示词"或"写第X章"时，母技能路由到 `novel-prompt`。
