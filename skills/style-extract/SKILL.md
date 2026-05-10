---
name: novel-style-extract
description: 文风提取。从参考小说中学习写作风格，提取量化规则和定性特征，合并到当前项目的写作配置中。Phase 2 增强路径。触发："学文风""提取风格""学习写作风格""参考小说""分析文风"。
---

# Novel Style Extract — 文风提取

> 摘要：统计脚本量化 → 定性 Agent 分层采样 → 主 Agent 合并注入 writing-style + anti-ai + few-shot 段落。

## Overview

从单本参考小说中提取写作风格，三步流程：统计脚本量化分析 → 定性 Agent 分层采样 → 主 Agent 合并注入。产出风格档案 + 更新当前项目的 writing-style.yaml、anti-ai.yaml 和提示词。

**When NOT to use:** 参考文本不存在、项目尚未初始化、作者只想手动调整写作风格。

**Announce at start:** "我来分析参考小说的文风。先跑统计分析..."

## 执行前提

Step 1 脚本 exit code 必须为 0。Step 2 outputs 必须包含原文引用。Step 3 合并后展示变更摘要，作者确认后写入。

## 前置条件

| 检查项 | 操作 |
|--------|------|
| 参考小说 .txt 文件存在？ | 不存在 → 询问作者提供文件路径 |
| 项目 story.yaml 存在？ | 不存在 → **STOP**，请先完成 Phase 1 初始化 |
| jieba + pyyaml 已安装？ | 未安装 → `pip3 install --break-system-packages jieba pyyaml` |

## Step 1: 统计分析脚本

运行 `scripts/analyze_style.py` 对参考文本做 12 项量化分析。

```bash
python3 ~/.claude/skills/awesome-novel/scripts/analyze_style.py <reference.txt> <project>/style-profiles/<name>/style-metrics.yaml
```

**12 项指标：**

| # | 指标 | 输出字段 |
|---|------|---------|
| 1 | 句长分布 | `sentence_length` — 短/中/长句占比、均值、标准差 |
| 2 | 句首词频 | `sentence_openings_top20` — 最常见的 20 种句首 |
| 3 | 段落统计 | `paragraph` — 段均长、中位数、单句段占比 |
| 4 | 对话占比 | `dialogue` — 引号内文字/总字数 |
| 5 | 标点密度 | `punctuation` — 句逗感叹省略号每千字密度 |
| 6 | 词频 | `word_frequency` — top200 高频词 + 副词/连词分类 |
| 7 | 成语密度 | `idiom_density` — 四字词每500字密度 |
| 8 | 形容词副词密度 | `adjective_adverb_density` — 每300字密度 |
| 9 | 环境描写占比 | `description_ratio` — 环境关键词+心理关键词估算 |
| 10 | 身体情绪密度 | `body_emotion_density` — 身体部位+情绪反应密度 |
| 11 | 句式癖好统计 | `structural_tic_usage` — 对 anti-ai.yaml 8 个模式的全文命中数 |
| 12 | 段首多样性 | `paragraph_opening_variety` — 段首词频率分布 |

脚本运行完成后展示简要摘要给作者。

## Step 2: 定性分析 Agent

启动一个 Agent，用分层采样策略阅读参考文本（~3-5万字），分析 6 个定性维度。

### 采样策略

| 层 | 来源 | 字数 | 目的 |
|----|------|------|------|
| 开篇 | 前 ~8000 字 | 8k | 开场策略、氛围建立 |
| 中段 | 随机 3 个 ~5000 字切片 | 15k | 日常习惯——对话节奏、描写密度 |
| 高潮 | 1-2 段高冲突区域（对话+情绪词密集区） | ~10k | 高压场景处理方式 |

### Agent 提示词

```
你是一位文学分析专家。你的任务是拆解一本小说的写作习惯，不是评价它好不好。

你要从以下 6 个维度分析所提供的文本样本：

1. 叙事距离 — 读者离角色多近？心理描写是直接写出来还是通过动作暗示？
   作者是否进入多个角色的内心？叙述者有没有直接"评语"？

2. 对话腔调 — 对话是书面腔还是口语腔？打断/省略/沉默的频率？
   对话标签习惯（"说/道/问" vs 动作标签 vs 副词标签）？角色说话有辨识度吗？

3. 描写偏好 — 环境描写是功能性的（只交代地点）还是氛围性的？五感偏好？
   比喻数量和类型（日常物品比喻 vs 自然比喻 vs 抽象比喻）？

4. 角色声音 — 不同角色的对话能否分辨？角色的身体反应是否各不同？
   次要角色是工具人还是有独立行为逻辑？

5. 情绪外化模式 — 写愤怒用哪些身体部位？写悲伤偏克制还是宣泄？
   情绪转折的铺垫密度（突然爆发 vs 层层累积）？

6. 禁忌与回避 — 这个作者不写什么？不写直白心理活动？不写长段环境？
   回避某些题材套路？不用某些词？

分析要求：
- 每条结论必须带上原文证据——引用原句（不超过 30 字）
- 禁止说空话（"文笔好""节奏感强"）——要可操作的结论
- 你是在拆解习惯，不是在写书评
```

### 同步任务：筛选 Few-shot 段落

Agent 在阅读时同步标记 8-12 个代表性段落：

| 类型 | 数量 | 用途 |
|------|------|------|
| 开场段落 | 1-2 | 展示作者的氛围建立方式 |
| 动作场景 | 2-3 | 展示动作描写的节奏和粒度 |
| 对话场景 | 2-3 | 展示对话的腔调和节奏 |
| 情绪场景 | 2 | 展示情绪外化的方式 |
| 过渡段落 | 1-2 | 展示场景切换/时间流逝处理 |

每个段落标注：`场景类型`、`展示的风格特征`（一句话）、`字数`。

### 输出文件

Agent 输出写入两个文件：

1. `style-profiles/{name}/style-qualitative.yaml` — 6 维分析结论
2. `style-profiles/{name}/examples.md` — 8-12 个标记段落

## Step 3: 主 Agent 合并

读取 Step 1 和 Step 2 的产出，合并到当前项目的写作配置中。

### 3a. 合并到 writing-style.yaml

原则：**只追加，不覆盖作者已确认的设定。**

| 来源 | 目标字段 | 策略 |
|------|---------|------|
| `style-metrics.sentence_length` | `natural_expression` | 比例→自然语言规则 |
| `style-metrics.paragraph_length` | `natural_expression` | 均值→段长约束 |
| `style-metrics.dialogue_ratio` | `natural_expression` | 对话密度指引 |
| `style-qualitative.叙事距离` | `pov_consistency` | 直接写入 |
| `style-qualitative.对话腔调` | `natural_expression` | 直接写入 |
| `style-qualitative.描写偏好` | `description_vs_depiction` | 追加技法偏好 |
| `style-qualitative.角色声音` | `character_building` | 追加角色规则 |
| `style-qualitative.情绪外化` | `depiction_techniques` | 追加或替换 |
| `style-qualitative.禁忌回避` | `possible_mistakes` | **追加**到列表末尾 |

冲突处理：统计数值 > 定性描述。数字不会撒谎。

### 3b. 校准 anti-ai.yaml

| 操作 | 内容 |
|------|------|
| 调整阈值 | 参考文本的 structural_tic 命中数 + 2 = 新阈值 |
| 追加疲劳词 | 参考文本中频率 < 2/10万字的词 → 加入 blocklist |
| 校准标点规则 | 参考文本的感叹号/省略号密度 → 更新阈值 |
| 校准段规则 | 参考文本的单句段占比 → 更新 `paragraph_rules` |

### 3c. 注入 Few-shot 到提示词

1. 在 `prompts/global-prompt.md` 新增"风格参考范例"段，放入全部 8-12 个参考段落
2. 在 chapter-loop Step 3 的章提示词中，按叙事段落 function 追加对应类型的参考段落：

| 叙事段落功能 | 注入的 example 类型 |
|-----------------|-------------------|
| `atmosphere` | 开场段落 |
| `dialogue_push` | 对话场景 |
| `action_beat` | 动作场景 |
| `emotional_landing` | 情绪场景 |
| `transition` | 过渡段落 |

### 3d. STOP: 展示变更摘要

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  文风提取完成：《{参考小说}》
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

writing-style.yaml 变更：
  + 新增 N 条 natural_expression 规则
  + 新增 N 条 pov_consistency 规则
  + 追加 N 项 possible_mistakes
  Δ 校准 N 项 depiction_techniques

anti-ai.yaml 变更：
  Δ 调整 N 个 structural_tic 阈值
  + 追加 N 个疲劳词

examples.md：
  已筛选 N 个参考段落，将注入提示词

确认后这些规则将应用到本章及后续所有章节的写作中。
```

作者确认后，写入文件，继续正常 Phase 流程。

## 输出文件结构

```
{project}/style-profiles/{name}/
├── style-metrics.yaml       # Step 1 脚本产出
├── style-qualitative.yaml   # Step 2 Agent 产出
└── examples.md              # Step 2 Agent 产出（few-shot 段落池）
```

## 下一步

文风提取完成后，回到正常写作流程。写作风格已按参考小说校准，后续的提示词生成（chapter-loop Step 3）和正文写作（chapter-loop Step 4）将自动应用提取到的规则和范例。
