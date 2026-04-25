---
name: novel-agent
description: 人类与AI协作写小说的工作流系统。触发条件：用户提到"写小说"、"创建小说项目"、"讨论设定"、"规划章节"、"生成正文"、"归档章节"。
---

# Novel Agent Skill

人类与AI协作写小说的工作流系统。

## Overview

Novel Agent 是一个小说创作工作流引导者，帮助作者从零开始完成小说的世界设定、角色塑造、情节规划，并通过 AI 生成高质量的章节内容。

核心原则：
- 过程文件全程 YAML 化，归档后为 Markdown
- Agent 与作者逐步讨论确认，每步可追溯
- 步步授权（默认）或全部授权模式

## When to Use

- 用户说"写小说"、"创建小说项目"
- 用户说"讨论世界设定"、"设计角色"
- 用户说"规划章节"、"写第X章"
- 用户说"生成正文"、"继续写"

**When NOT to use:** 用户只是想聊小说内容、不需要系统化工作流。

## Process

### Phase 1: Init - 创建项目

触发条件：用户说"create novel [项目名]"或"创建小说项目 [项目名]"

步骤：
1. 执行 `python scripts/init.py [项目名] [--author 作者名]`
2. 脚本创建目录结构并复制 story.yaml、world-setting.yaml、writing-style.yaml 模板
3. 询问作者 title 和 author（若未通过 --author 传入）
4. 将 title、author、created_at 写入 story.yaml
5. 告知用户 `cd [项目名]` 进入项目目录
6. 提示作者：写作风格指南已预填默认设定（Show Don't Tell、客观叙事、禁止道德说教等），可在下一阶段审视调整

### Phase 2: 设定阶段 - 世界 & 角色 & 写作风格

触发条件：Phase 1 完成，作者说开始设定

本阶段完成三项设定：世界设定、角色设定、写作风格确认。顺序不可跳过。

世界设定讨论:
1. 用 AskUserQuestion 问世界类型（玄幻/科幻/悬疑/都市/其他）
2. 逐领域用自然语言引导描述：geography → politics → culture → history → rules → physics → biology → sociology
3. 每领域讨论完即时总结确认
4. 全部确认后写入 settings/world-setting.yaml

角色设定讨论:
1. 用 AskUserQuestion 收集角色名列表（multiSelect 选 story_role 类型）
2. 逐角色讨论，每个角色讨论以下维度：
   - cognition (认知方式：角色如何理解和处理信息)
   - worldview (世界观：角色对世界的根本看法)
   - self_identity (自我定位：角色如何定义"我是谁")
   - values (价值观：角色认为什么重要、什么不重要)
   - abilities (能力：天赋、特长、超凡力量等)
   - skills (技能：后天习得的技艺)
   - environment (所处环境：物理和社会环境对角色的塑造)
3. story_role 枚举值：protagonist / antagonist / supporting / minor
4. 每角色讨论完创建 `settings/character-setting/[角色名拼音id].yaml`

写作风格确认（世界和角色设定完成后进行）:
1. 告知作者：settings/writing-style.yaml 已预填默认写作原则，包括：
   - 角色定位：全球闻名的客观冷峻小说作家
   - Show Don't Tell：禁止直接描写感受，通过动作/语言/微表情展示
   - 禁止道德说教：让故事和角色自己说话
   - 禁止俗套比喻：拒绝"眼泪像断了线的珍珠"之类表达
   - 五种描写技法：动作描写、对话展示、微表情捕捉、环境互动、内心独白
2. 用 AskUserQuestion 询问作者是否调整：
   - "使用默认风格，以后再说" — 跳过
   - "我想调整一些地方" — 逐项讨论修改
   - "我想用自己的风格" — 开放讨论，重写 writing-style.yaml
3. 如果作者选择调整，修改 settings/writing-style.yaml 并确认

### Phase 3: 故事线拆分 + 卷纲 + 章纲

触发条件：用户确认设定阶段完成

流程（以卷1为例）:
1. 创建 `volumes/volume-1.yaml`，写入卷标题和卷概要
2. 讨论卷纲：本卷核心冲突、主要事件、角色弧光走向
3. 将章节摘要列表写入 volume-1.yaml 的 chapters_summary
4. 逐章讨论章纲 → 创建 `chapters/vol-1-ch-1.yaml`
5. 重复直到本卷所有章纲完成
6. 更新 story.yaml 的 volumes 和 chapters 列表
7. 进入下一卷，直到所有卷规划完成

章纲内容（chapter.yaml 字段）:
- outline.summary: 本章核心情节点
- outline.key_points: 本章要点列表
- outline.characters: 本章涉及的角色列表（引用角色 yaml 文件名）
- outline.location: 场景地点
- outline.time: 时间背景

章状态（chapter.status）:
- `outline` — 章纲已确认，等待生成提示词
- `draft` — 提示词已生成，等待正文生成
- `archived` — 正文已归档

卷与章的关系以 story.yaml 的 chapters 列表为唯一数据源，volume.yaml 的 chapters_summary 仅作为规划阶段的摘要参考。

### Phase 4: 提示词生成

触发条件：章状态为 outline 且章纲获作者确认

步骤：
1. 读取以下源文件（详见下方映射表）
2. 按映射表组装提示词 yaml
3. 提供 3 个提示词变体供作者选择（同一章纲内容 + 3 种不同切入角度/叙事策略）
4. 作者不满意则调整
5. 确认后将章节状态从 outline → draft
6. 确保 `chapters/prompts/` 目录存在，保存为 `chapters/prompts/vol-N-ch-M-prompt.yaml`

**提示词组装映射表**（源文件 → 提示词字段）:

| 读取的源文件 | 映射到提示词字段 | 说明 |
|-------------|-----------------|------|
| writing-style.yaml > role | `role` | 直接复用 |
| writing-style.yaml > core_principles | `core_principles` | 直接复用 |
| writing-style.yaml > possible_mistakes | `possible_mistakes` | 直接复用 |
| writing-style.yaml > depiction_techniques | `depiction_techniques` | 直接复用 |
| world-setting.yaml > details | `context.world_setting` | 整个 details 块 |
| character-setting/[角色].yaml | `context.characters[]` | 仅包含本章出场的角色 |
| volume-N.yaml | `context.plot` | 本卷冲突、主线 |
| chapter.yaml > outline | `content` | 章纲内容作为写作素材 |
| chapter.yaml > outline.location + time | `context.scene` | 场景时间和地点 |

**3个变体的生成策略**（同一章纲，不同切入角度）:
- 变体1: 以主角视角展开，侧重内心活动和角色体验
- 变体2: 以场景氛围开场，侧重环境描写和节奏铺陈
- 变体3: 以冲突/事件切入，侧重动作和对话推进

作者也可要求其他角度。

### Phase 5: 正文生成

触发条件：提示词 yaml 已获作者确认

步骤：
1. 主 Agent 用 Agent 工具（subagent_type: "general-purpose"）启动 subagent 写正文
2. subagent 的 prompt 为：读取提示词 yaml 路径，严格按其中的 role、core_principles、context、content 写作，一次性生成完整章节正文
3. subagent 返回正文
4. 主 Agent 将正文展示给作者审阅
5. 作者修改意见由主 Agent 直接编辑正文（不重新调用 subagent）
6. 作者满意后，将章节状态从 draft → archived

Subagent 调用示例：
```
Agent(
  description: "生成第{N}卷第{M}章正文",
  subagent_type: "general-purpose",
  prompt: "读取 chapters/prompts/vol-{N}-ch-{M}-prompt.yaml，严格按照其中的 role、core_principles、context、content 字段写作。一次性生成完整章节正文，不少于1000字。只返回正文内容。"
)
```

### Phase 6: 归档

触发条件：作者审阅正文满意，确认归档

步骤：
1. 将正文写入 `archives/vol-{N}-ch-{M}-{slugified-title}.md`
2. 分析正文中角色的变化（位置、关系、能力、心态），推断状态更新
3. 为每个出场角色追加 state_history 条目（见下方格式）
4. 同步更新角色 yaml 中受影响的当前状态字段，对照清单：
   - `location` / `environment` 是否变化
   - `abilities` / `skills` 是否变化（突破、获得新能力）
   - `relationships[].status` 是否变化（关系亲疏、立场转变）
   - `worldview` / `self_identity` 是否因本章事件产生偏移
   - `summary` 是否需要改写以反映角色当前状态
5. 将 chapter.yaml 的 status 更新为 `archived`
6. 更新 story.yaml 的 chapters 列表中对应条目

角色 state_history 格式（追加到 character yaml 的 state_history 数组末尾）:
```yaml
state_history:
  - after_volume: 1
    after_chapter: 1
    location: "角色当前位置"
    status: "角色当前状态简述"
    changes:
      - "具体变化1"
      - "具体变化2"
```

story.yaml chapters 条目 schema（归档后更新）:
```yaml
chapters:
  - id: "1-1"
    volume: 1
    chapter: 1
    title: "章节标题"
    path: "./chapters/vol-1-ch-1.yaml"
    archive_path: "./archives/vol-1-ch-1-章节标题.md"
    status: "archived"
```

## 提示词 YAML 格式

提示词 yaml 由 Agent 生成，包含完整上下文供 subagent 独立写作：

```yaml
prompt_version: "1.0"
chapter_ref:
  volume: 1
  chapter: 1
  title: "第1章标题"

role: |
  你是全球闻名的小说作家...

core_principles:
  global_rules:
    - "客观对待，不带道德化..."
    - "保持世界观逻辑推进..."
  natural_expression: [...]
  description_vs_depiction: [...]
  character_building: [...]

possible_mistakes: [...]

depiction_techniques: [...]

context:
  world_setting: {...}
  characters: [...]
  plot: {...}
  scene: {...}

content: |
  [章纲内容]
```

## 授权模式

- **步步授权（默认）**: 每步需作者确认
- **全部授权**: Agent 全权决定

作者可随时说"你全权决定"或"每步都要我确认"切换模式。

## Common Rationalizations

- "作者没回应我就继续往下走" → 必须等待确认
- "章纲差不多就行，不用那么详细" → 细节决定质量
- "角色设定差不多了，直接开始写" → 基础不牢地动山摇
- "提示词生成完不用给作者选了" → 作者选择权是核心流程

## Red Flags

- 跳过 Phase 2 直接进入 Phase 3
- 不更新 story.yaml 就往下走
- subagent 生成正文时上下文不完整
- 正文写完不归档就直接结束
- 不更新角色 state_history

## Verification

检查清单：
- [ ] story.yaml 存在且包含正确的项目信息
- [ ] 每个设定阶段都有作者确认记录
- [ ] 章纲包含所有必需字段 (summary, key_points, characters, location, time)
- [ ] 提示词 yaml 包含完整上下文
- [ ] 归档后的 markdown 命名正确 (vol-{N}-ch-{M}-{title}.md)
- [ ] 角色 state_history 在归档时更新

