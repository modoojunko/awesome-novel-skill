---
name: novel-write
description: 正文生成与质量检查。Phase 5。按 segment 串行调 subagent 写正文，拼接后执行 15 项质量检查和深度评审，通过后展示给作者。触发："写正文""写第X章""继续写""生成正文""质量检查"。必须确认 segment 提示词已存在才能使用。
---

# Novel Write — 正文生成与质量检查

## Overview

按叙事功能段落（segment）串行调 subagent 写正文，每个 subagent 只承担 400-600 字的小任务。拼接后执行 15 项硬性质量检查 + 10 维深度评审，正文和评审报告一起展示给作者。

**When NOT to use:** segment 提示词不存在、正文已生成且通过质量检查、章状态不是 draft。

**Announce at start:** "我来生成第{N}卷第{M}章正文。共 {S} 个段落，串行写作。"

## HARD-GATE

```
正文必须先通过全部质量检查，才能展示给作者。
任意一项触发 → 不展示正文，报告问题，由作者决定下一步。
```

## 进入门禁

| 检查项 | 操作 |
|--------|------|
| `prompts/vol-{N}-ch-{M}-seg-{1}-prompt.md` 存在？ | 不存在 → **STOP**，退回 `novel-prompt` |
| chapter.yaml segments 非空？ | 空 → **STOP**，退回 `novel-prompt` Step 0 先拆 segment |
| chapter.yaml status = draft？ | 不是 → **STOP**，检查前面 Phase 是否完成 |

## Step 1: 串行 Subagent 写各 Segment

读取 chapter.yaml 的 segments 列表，按序号串行执行。

```
for seg in 1..N:
    # 1. 读取本段提示词
    prompt_file = prompts/vol-{N}-ch-{M}-seg-{S}-prompt.md
    
    # 2. 若 seg ≥ 2，将 {%%PREV_SEGMENT_ENDING%%} 替换为上一段的实际结尾 200 字
    if seg >= 2:
        读取 prompt_file
        找到 {%%PREV_SEGMENT_ENDING%%}
        替换为：
        "上一段结尾原文（从这里接）：
        > {prev_segment_last_200_chars}"
        写回 prompt_file
    
    # 3. 调 subagent（模型从 settings/writing-style.yaml 的 writing_model 读取）
    Agent(
      description: "写第{N}卷第{M}章 Segment {S}/{N}",
      subagent_type: "general-purpose",
      model: "{writing_model}",
      prompt: "读取 {prompt_file}。该文件是你的完整写作指令——包含全局写作方法论、故事背景、本段写作指引。

严格按文件中的所有要求写作。字数必须达到 word_target 指定的目标（不低于 80%，不超过 120%）。

关键约束：
- 你只写这一段，不写整章。段长 {word_target} 字左右。
- 如果写作指引中有'上一段结尾原文'，你的第一句话必须从那个画面无缝接续。不要复述或总结上一段内容——直接接着往下写。
- 结尾必须停在 ends_with 指定的画面/状态。不要超出，不要写下一段的内容。
- 只输出小说正文。禁止出现解释、说明、注释、'以下是正文'等引导语。从第一个字开始就是小说正文，最后一个字结束就是段落结束。
"
    )
    
    # 4. 提取本段结尾 200 字，供下一段使用
    prev_segment_last_200_chars = subagent输出的最后 200 个字符
```

**段落衔接规则：**
- Segment 1 无上一段——提示词中无 {%%PREV_SEGMENT_ENDING%%} 占位符
- Segment 2..N：上一段结尾 200 字注入后，subagent 第一句话必须自然接续
- 主 Agent 不在段之间添加任何过渡文字——subagent 自己负责从上一段结尾接续

## Step 2: 拼接 + 质量检查 + 深度评审

所有 segment 写完并通过各段字数检查后：

### 2a. 拼接正文

将 seg-1 到 seg-N 的输出按序拼接，段间不加任何分隔符或过渡语。保存为临时全文。

### 2b. 15 项质量检查

对拼接后的全文执行以下检查。检测依据：`settings/anti-ai.yaml` 的 8 个规则组。

| # | 检查项 | 不通过处理 |
|---|--------|-----------|
| 1 | 字数不达标 | 报告实际字数 vs 要求，列出各 segment 字数分布 |
| 2 | 上帝视角摘要 | 摘出典型句，特别检查 segment 衔接处是否出现了"接着""然后""与此同时"等生硬过渡词 |
| 3 | 违反核心约束 | 指出违规条款和位置 |
| 4 | 夹带非正文内容 | 指引导语、解释、文末总结 |
| 5 | AI疲劳词触发 | 扫描 fatigue_words，报告风险等级。严重级（元叙事/上帝视角词）必须重写对应 segment |
| 6 | AI句式违规 | 连续同结构开头、列表式叙述、说明书式对话 |
| 7 | 结构性句式癖好 | grep 扫描 structural_tic_patterns，超阈值报告（模式名 + 命中次数 + 阈值） |
| 8 | 章尾情绪缺口 | Segment N（emotional_landing）是否留下了有效钩子？无 → "缺钩子——读者没有继续阅读的理由" |
| 9 | 情绪兑现检测 | pay_off旧缺口 → 正文有兑现段？make_new缺口 → 结尾有新问题？ |
| 10 | 跨章情绪单调 | 最近 3-5 章 primary_mood 连续相同？同种钩子类型？ |
| 11 | 微兑现缺失 | 本章至少一处"有收获"段落？过渡章达标？对照 segments 中的 micro_payoff 字段 |
| 12 | 安全着陆 | 结尾所有冲突完美解决？→ "读者没有点下一章的理由" |
| 13 | 物品/状态一致性 | 跨 segment 检查——物品消耗后仍出现？突然出现未交代物品？场景切换物品状态合理？ |
| 14 | 句式单调检测 | 连续 4 句相同主语/连词开头？短句(<10字)和长句(>50字)数量达标？ |
| 15 | 身体反应模板化 | "眼神/心里/喉咙/手心"密度 > 5次/500字？跨 segment 统计。同一反应被不同角色复用？ |

**句式癖好检测方法：**
```bash
grep -cP '不是.{1,20}(而是|，是|,是)' archives/vol-00N-ch-00M-*.md
```
对照 anti-ai.yaml structural_tic_patterns 每个模式的 threshold。

任意一项触发 → **不展示正文**，报告问题，由作者决定：重写单个 segment / 重写全章 / 手动修改。

### 2c. 深度评审

全部 15 项质量检查通过后，触发 `novel-review` 进行 10 维 60+ 细项诊断。评审报告与正文一起展示给作者。

## Step 3: 作者审阅

将拼接后的正文全文 + novel-review 评审报告一起展示给作者。

**展示格式：**
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
- "满意，归档" → Phase 6（`novel-archive`）
- "修改第X段" → 指定修改意见，主 Agent 直接编辑拼接后的正文对应位置
- "重写 seg-X" → 对该 segment 单独重新调 subagent（注入 seg-(X-1) 实际结尾作为锚点），写完后重新拼接、重新质量检查
- "重写全章" → 所有 segment 重新串行生成

## 下一步

作者满意后说"归档"→ Phase 6（`novel-archive`）。需修改时说"修改第X段"或"重写 seg-X"。需重新生成时说"重写全章"。
