---
name: novel-write
description: 正文生成与质量检查。Phase 5。一个 subagent 读全部 segment 提示词写全章，15 项质量检查和深度评审通过后展示给作者。触发："写正文""写第X章""继续写""生成正文""质量检查"。必须确认 segment 提示词已存在才能使用。
---

# Novel Write — 正文生成与质量检查

## Overview

一个 subagent 读本章全部 segment 提示词和 chapter.yaml 章纲，一次性写完整章正文。写完后执行 15 项硬性质量检查 + 10 维深度评审，正文和评审报告一起展示给作者。

**When NOT to use:** segment 提示词不存在、正文已生成且通过质量检查、章状态不是 draft。

**Announce at start:** "我来写第{N}卷第{M}章正文。"

## HARD-GATE

```
正文必须先通过全部质量检查，才能展示给作者。
任意一项触发 → 不展示正文，报告问题，由作者决定下一步。
```

## 进入门禁

| 检查项 | 操作 |
|--------|------|
| `prompts/vol-{N}-ch-{M}-seg-{1}-prompt.md` 存在？ | 不存在 → **STOP**，退回 `novel-prompt` |
| chapter.yaml status = draft？ | 不是 → **STOP**，检查前面 Phase 是否完成 |

## Step 1: 派 exec-prose 写全章

读 `agents/pipeline/exec-prose.md` 获取 agent 定义，构造 prompt 注入章号和巻号参数，派发单个 Agent tool 调用。

```
Agent(
  agent_file: "agents/pipeline/exec-prose.md",
  model: "{writing_model}",
  context: {
    volume: {N},
    chapter: {M},
    total_words: {total_words}
  },
  prompt: "
【写作要求补充】
- 字数 {total_words} 字左右
- 按 seg-1 → seg-N 的自然顺序写，段落间过渡流畅
- 每个 segment 的写作指引必须兑现
- 结尾停在最后一段的 ends_with 指定画面/状态
"
)
```

写完后，文件保存在：
  `archives/vol-{N}-ch-{M}-{slug}.draft.md`
  作者可随时打开此文件审阅草稿。

## Step 2: 质量检查 + 深度评审

对生成的全文执行以下检查。检测依据：`settings/anti-ai.yaml` 的 8 个规则组。

| # | 检查项 | 不通过处理 |
|---|--------|-----------|
| 1 | 字数不达标 | 报告实际字数 vs 要求 |
| 2 | 上帝视角摘要 | 摘出典型句 |
| 3 | 违反核心约束 | 指出违规条款和位置 |
| 4 | 夹带非正文内容 | 指引导语、解释、文末总结 |
| 5 | AI疲劳词触发 | 扫描 fatigue_words，报告风险等级。严重级必须重写对应位置 |
| 6 | AI句式违规 | 连续同结构开头、列表式叙述、说明书式对话 |
| 7 | 结构性句式癖好 | grep 扫描 structural_tic_patterns，超阈值报告（模式名 + 命中次数 + 阈值） |
| 8 | 章尾情绪缺口 | 章末是否留下了有效钩子？无 → "缺钩子——读者没有继续阅读的理由" |
| 9 | 情绪兑现检测 | pay_off旧缺口 → 正文有兑现段？make_new缺口 → 结尾有新问题？ |
| 10 | 跨章情绪单调 | 最近 3-5 章 primary_mood 连续相同？同种钩子类型？ |
| 11 | 微兑现缺失 | 本章至少一处"有收获"段落？过渡章达标？对照 segments 中的 micro_payoff 字段 |
| 12 | 安全着陆 | 结尾所有冲突完美解决？→ "读者没有点下一章的理由" |
| 13 | 物品/状态一致性 | 物品消耗后仍出现？突然出现未交代物品？场景切换物品状态合理？ |
| 14 | 句式单调检测 | 连续 4 句相同主语/连词开头？短句(<10字)和长句(>50字)数量达标？ |
| 15 | 身体反应模板化 | "眼神/心里/喉咙/手心"密度 > 5次/500字？同一反应被不同角色复用？ |

**句式癖好检测方法：**
```bash
grep -cP '不是.{1,20}(而是|，是|,是)' archives/vol-00N-ch-00M-*.md
```
对照 anti-ai.yaml structural_tic_patterns 每个模式的 threshold。

任意一项触发 → **不展示正文**，报告问题，由作者决定：重写全章 / 手动修改。

### 深度评审

全部 15 项质量检查通过后，主 Agent 直接执行 `novel-review`——10 维 60+ 细项诊断。主 Agent 已持有全部上下文（正文、章纲、角色文件、设定文件等），无需额外 subagent 开销。评审报告与正文一起展示给作者。

## Step 3: 作者审阅

将正文全文 + novel-review 评审报告一起展示给作者。

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
- "修改第X段" → 指定修改意见，主 Agent 直接编辑正文对应位置
- "重写全章" → 重新调 subagent 写全章，重新质量检查

## 下一步

作者满意后说"归档"→ Phase 6（`novel-archive`）。需修改时说"修改第X段"。需重新生成时说"重写全章"。
