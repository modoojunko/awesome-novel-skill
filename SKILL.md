---
name: novel-agent
description: 人类与AI协作写小说的工作流系统。触发条件：用户提到"写小说"、"创建小说项目"、"讨论设定"、"规划章节"、"生成正文"、"归档章节"。
---

<!--
awesome-novel-skill - AI-assisted novel writing workflow system
Copyright (C) 2026  modoojunko

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
-->

# Novel Agent Skill

人类与AI协作写小说的工作流系统。

## Overview

Novel Agent 是一个小说创作工作流引导者，帮助作者从零开始完成小说的世界设定、角色塑造、情节规划，并通过 AI 生成高质量的章节内容。

核心原则：
- 过程文件全程 YAML 化，归档后为 Markdown
- Agent 与作者逐步讨论确认，每步可追溯
- 步步授权（默认）或全部授权模式
- **Agent 是引导者，不是代笔机器。所有 YAML 文件和正文必须经过与作者的讨论确认后才能写入。严禁看到模板格式就自行填充生成。**

## When to Use

- 用户说"写小说"、"创建小说项目"
- 用户说"导入小说"、"导入已有作品"、"续写已有小说"
- 用户说"讨论世界设定"、"设计角色"
- 用户说"规划章节"、"写第X章"
- 用户说"生成正文"、"继续写"

**When NOT to use:** 用户只是想聊小说内容、不需要系统化工作流。

## Process

### Phase 0: 导入已有小说（可选）

触发条件：用户说"导入小说"、"导入已有作品"、"续写已有小说"

这是一个替代 Phase 1-3 的快速入口，适用于已经有成文内容的作者。Agent 通过分析已有正文，反向提取设定，免去从零讨论的步骤。

步骤：

1. 执行 Phase 1（init），创建项目骨架
2. 请作者提供已有小说文件（支持 .txt / .md 格式，单文件或多文件均可）
3. 执行 `python scripts/import.py [项目路径] [小说文件]` 自动切分章节、写入 archives/ 和 chapters/
4. Agent 逐章阅读正文，反向提取以下信息：
   - **世界设定**：从正文中推断世界观类型、地理、社会规则等，写入 `settings/world-setting.yaml`
   - **角色设定**：识别出场角色，从正文中提取其认知方式、价值观、能力等六层维度，写入 `settings/character-setting/`
   - **写作风格**：分析正文的叙事习惯（用词偏好、句式特征、对话风格），写入 `settings/writing-style.yaml`
   - **钩子追踪**：识别已有伏笔和未解决线索，写入 `settings/hooks.yaml`
5. 为每章创建 `chapters/vol-N-ch-M.yaml` 章纲（根据已有正文反写 outline）
6. 创建 `volumes/volume-N.yaml` 卷纲
7. 更新 `story.yaml` 索引
8. 确认当前进度（已写了几卷几章），后续从 Phase 4 开始继续创作

导入模式的特殊约定：
- 反向提取的设定必须经作者确认后才能定稿——Agent 不假设自己理解正确
- 如果正文中某个设定不明显，Agent 应向作者提问而非自行推测
- 导入完成后，状态等同于 Phase 3 完成，可直接进入 Phase 4 写后续章节

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

本阶段完成世界设定、角色设定、写作风格确认、题材选择和钩子初始化。顺序不可跳过。

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

题材配置（写作风格确认后进行）:
1. 引导作者确定题材类型（玄幻/仙侠/都市/科幻/悬疑/恐怖/同人/其他）
2. 讨论题材特定的爽点类型、章节类型偏好、节奏红线
3. 讨论该题材的反套路规则（读者已厌倦的套路，需避开）
4. 将讨论结果写入 settings/writing-style.yaml 的 genre 字段

钩子初始化（题材配置后进行）:
1. 引导作者浏览 settings/hooks.yaml，了解钩子生命周期和操作语义
2. 如果作者有已知伏笔想法，写入 hooks 列表；否则留空随章纲讨论时逐步填充
3. hooks.yaml 在后续 Phase 3/5/6 中持续更新

### Phase 3: 故事线拆分 + 卷纲 + 章纲

触发条件：用户确认设定阶段完成

流程（以卷1为例）:
1. 创建 `volumes/volume-1.yaml`，写入卷标题和卷概要
2. 讨论卷纲：本卷核心冲突、主要事件、角色弧光走向
3. 将章节摘要列表写入 volume-1.yaml 的 chapters_summary
4. 逐章讨论章纲 → 创建 `chapters/vol-1-ch-1.yaml`
   - 讨论章纲时，同步讨论本章的钩子操作：
     - 本章是否埋下新伏笔？（upsert）
     - 本章是否提及/推进已有伏笔？（mention）
     - 本章是否收束某个伏笔？（resolve）
   - 更新 settings/hooks.yaml 中受影响的钩子条目
5. 重复直到本卷所有章纲完成
6. 更新 story.yaml 的 volumes 和 chapters 列表
7. 进入下一卷，直到所有卷规划完成

### 控制文档（可选，随时更新）

项目根目录下的 `author-intent.md` 和 `current-focus.md` 是作者直接表达意图的轻量级文档，不经过 YAML 结构化。

- **author-intent.md**：长周期方向。核心主题、终局设想、写作信条、绝不妥协的底线、长期伏笔池。Agent 在每次 Phase 3 章纲讨论和 Phase 4 视角转换时都应读取此文件。
- **current-focus.md**：接下来 1-3 章的聚焦。当前优先级、需推进的支线、需提及的钩子、节奏意图、限制约束。Agent 在 Phase 3 章纲讨论和 Phase 4 第一轮视角转换时必须读取此文件。

作者可以随时说"更新作者意图"或"更新当前聚焦"来修改这两个文件。Agent 应主动引导作者在每写完 3-5 章后审视并更新 current-focus.md。

章纲内容（chapter.yaml 字段）:
- outline.summary: 本章核心情节点
- outline.key_points: 本章要点列表
- outline.characters: 本章涉及的角色列表（引用角色 yaml 文件名）
- outline.location: 场景地点
- outline.time: 时间背景

章状态（chapter.status）:
- `outline` — 章纲已确认，等待生成提示词
- `draft` — 提示词已生成，正文写作/修改中，等待归档
- `archived` — 正文已归档

卷与章的关系以 story.yaml 的 chapters 列表为唯一数据源，volume.yaml 的 chapters_summary 仅作为规划阶段的摘要参考。

### Phase 4: 提示词生成

触发条件：章状态为 outline 且章纲获作者确认

本阶段分两轮进行，每轮必须等作者确认后才能进入下一步。**严禁在作者确认视角转换前提前生成提示词变体。**

**第一轮：视角转换**

1. 读取章纲 `chapters/vol-N-ch-M.yaml` 的 outline 字段
2. 按视角转换规则（见下方）将上帝视角章纲转换为沉浸式写作指引
3. **STOP：将转换后的内容展示给作者，等待确认。作者不满意则继续调整，直到确认。**
4. 作者确认视角转换后，进入第二轮。

**第二轮：组装提示词并生成变体**

5. **必须先读取 `settings/writing-style.yaml`**，将其中的 `role`、`core_principles`、`possible_mistakes`、`depiction_techniques` 四个字段的内容融合为自然段落（见下方提示词格式）。这四个字段是 subagent 的行为约束，缺失任何一个 subagent 都会放飞。
   - **同时读取 `skill_layers` 字段**：L1 结构层原则用于增强第一轮视角转换的叙事约束，L2 内容层技法融入"写作原则与禁忌"段，L3 审查层维度保留用于 Phase 5 质量检查。三层各司其职，不全部塞给 subagent。
   - **同时读取 `genre` 字段**：题材的爽点类型、节奏红线融入"写作要求"段，反套路规则融入"写作原则与禁忌"段。
6. 读取其余源文件，按映射表将各来源内容转为自然段落
7. 将第一轮确认后的沉浸式内容作为"写作指引"段写入
8. 基于同一 content，生成 3 个提示词变体（不同切入角度/叙事策略）
9. **STOP：将 3 个变体展示给作者选择，作者不满意则调整，直到确认。**
10. 作者确认后，将章节状态从 outline → draft
11. 确保 `prompts/` 目录存在，保存为 `prompts/vol-N-ch-M-prompt.md`

**提示词组装映射表**（源文件 → 提示词 prose 段落）:

| 读取的源文件 | 映射到提示词字段 | 说明 |
|-------------|-----------------|------|
| writing-style.yaml > role | 角色定位段 | 原样写入 |
| writing-style.yaml > core_principles + possible_mistakes + depiction_techniques | 写作原则与禁忌段 | 融合为自然段落 |
| world-setting.yaml > details | 故事背景段 | 融合为叙述 |
| character-setting/[角色].yaml | 故事背景段 | 角色当前状态，融入背景叙述 |
| volume-N.yaml | 故事背景段 | 本卷冲突、主线，融入背景叙述 |
| chapter.yaml > outline.location + time | 场景段 | 场景时空 |
| chapter.yaml > outline | 写作指引段 | 章纲经视角转换后填入（见下方规则） |

**视角转换规则**（章纲 → 提示词 content 字段）——一句话概括：

> **把"发生了什么事"重写为"事情发生时，在场的人感受到了什么"——前者是给作者看的，后者才是给 subagent 写的。**

转换要求：
- 禁止在 content 中出现"本章讲述了""主角经历了""剧情推进到"等上帝视角概述语
- 将章纲的事件概要改写为场景化指引：从谁的视角出发、看到了什么、感受到了什么、发生了什么冲突
- 用具体可感的细节替代抽象总结，比如"两人决裂"应变为"对话中逐渐积累的误解在某个瞬间爆发，两人各自的选择将关系推向不可挽回的方向"
- content 应是"让作者沉浸到场景中去写"的指引，而非"告诉 subagent 剧情是什么"的摘要
- **指引不是剧本。禁止按时间顺序逐段描述'先写什么再写什么'。给出氛围基调、关键情节点、情感走向即可，把具体的叙事节奏、细节选择和语言组织留给 subagent。如果 content 读起来像分镜脚本，说明粒度太细了。**
- 禁止自由发挥联想，严格基于章纲已确认的情节，仅改变叙述视角，不添加章纲中没有的事件

**3个变体的生成策略**（同一章纲，不同切入角度）:
- 变体1: 以主角视角展开，侧重内心活动和角色体验
- 变体2: 以场景氛围开场，侧重环境描写和节奏铺陈
- 变体3: 以冲突/事件切入，侧重动作和对话推进

作者也可要求其他角度。

### Phase 5: 正文生成

触发条件：提示词已获作者确认

步骤：
1. 主 Agent 用 Agent 工具（subagent_type: "general-purpose"）启动 subagent 写正文
2. subagent 的 prompt 必须包含以下硬性约束（见下方完整示例）——注意提示词文件已是 prose 格式，subagent 直接阅读即可，不需解析 YAML 结构
3. subagent 返回正文后，主 Agent 先做质量检查（见下方判断标准），不合格则向作者报告问题，由作者决定如何处理
4. 质量合格后，主 Agent 将正文展示给作者审阅
5. 作者修改意见由主 Agent 直接编辑正文（不重新调用 subagent）
6. 作者满意后，将正文写入 `archives/vol-{N}-ch-{M}-{slugified-title}.md`（草稿落盘）
7. 进入 Phase 6 归档流程

**Subagent 调用模板**（prompt 字段必须逐字包含以下所有约束）：

```
Agent(
  description: "生成第{N}卷第{M}章正文",
  subagent_type: "general-purpose",
  prompt: "读取 prompts/vol-{N}-ch-{M}-prompt.md。该文件是你的完整写作指令，从角色定位到场景细节到字数要求全部包含在内。

严格按文件中的所有要求写作：
1. 文件中已包含写作风格约束、常见错误清单、描写技法指南——每一条都必须遵守。
2. 文件中已包含场景基调、关键节点、叙述约束和写作要求。写作要求中的字数下限为硬性指标，低于此字数视为不合格。
3. 禁止以下句式和行为：
   - 禁止'他感到''他觉得''他意识到'等直接描述情绪或认知的句式——用身体反应、动作、环境互动替代
   - 禁止'本章讲述了''接下来'等元叙事语句
   - 禁止在文末进行任何总结、升华、点评
   - 禁止使用俗套比喻
   - 禁止用副词修饰对话（如'她愤怒地说'），对话本身传达情绪
4. 只输出正文本身。输出中禁止出现任何解释、说明、注释、前缀、后缀、'以下是正文'或类似引导语。从第一个字开始就是小说正文，最后一个字结束就是小说结束。"
)
```

**放弃 subagent 输出的判断标准**：

subagent 返回的正文在展示给作者之前，主 Agent 必须先检查以下六项（含两项 AI 味检测）。**任意一项触发，不展示正文，向作者报告具体问题，由作者决定下一步：重新调用 subagent、主 Agent 按指令重写、或作者给出方向后主 Agent 修改。**

检测时参考 `settings/anti-ai.yaml` 中的 fatigue_words、sentence_rules、paragraph_rules、dialogue_rules 四个规则组。

| 触发条件 | 报告内容 |
|---------|---------|
| 字数不达标 | 告知作者：实际字数 vs 要求字数下限，询问是否接受当前长度还是重写 |
| 上帝视角摘要 | 摘出正文中典型的概述句式（如"他经历了""本章讲述了"），向作者说明为什么这些段落读起来像梗概而非叙事，询问是否按提示词要求重写 |
| 违反核心约束 | 指出正文中违反的具体约束条款（引用提示词文件中的禁止条目），说明违规位置 |
| 夹带非正文内容 | 指出正文前后的引导语、解释、或文末的总结升华段落 |
| AI疲劳词触发 | 对照 `settings/anti-ai.yaml` 的 fatigue_words 列表扫描正文，统计高频疲劳词出现次数和位置，向作者报告风险等级（严重/高/中/低）。严重级（元叙事、上帝视角词）必须重写。**
| AI句式违规 | 检测连续同结构开头、列表式叙述、说明书式对话，向作者报告违规位置和建议改法 |

### Phase 6: 归档

触发条件：作者审阅正文满意，确认归档

步骤：
1. 正文已在 Phase 5 写入 `archives/vol-{N}-ch-{M}-{slugified-title}.md`，此步复核归档文件内容无误
2. 分析正文中角色的变化（位置、关系、能力、心态），推断状态更新
3. 为每个出场角色追加 state_history 条目（见下方格式）
4. 同步更新角色 yaml 中受影响的当前状态字段，对照清单：
   - `location` / `environment` 是否变化
   - `abilities` / `skills` 是否变化（突破、获得新能力）
   - `relationships[].status` 是否变化（关系亲疏、立场转变）
   - `worldview` / `self_identity` 是否因本章事件产生偏移
   - `summary` 是否需要改写以反映角色当前状态
5. 更新 hooks.yaml：检查本章内容中是否有钩子被提及、推进或收束，执行对应操作（mention/resolve/defer），更新 last_mentioned_chapter 和 status 字段
6. 运行钩子健康检查（参考 hooks.yaml 的 hook_health_rules）：
   - 是否有超过陈旧阈值的高优先级钩子？
   - 是否有本章集中收束超过 3 个钩子的情况？
   - 将检查结果报告给作者
7. 将 chapter.yaml 的 status 更新为 `archived`
8. 更新 story.yaml 的 chapters 列表中对应条目

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

## 提示词格式

提示词保存为 `prompts/vol-N-ch-M-prompt.md`，**必须是自然语言 prose 格式，不是 YAML 结构**。原因：subagent 是 LLM，prose 指令比结构化碎片更有效——它不需要先在脑内拼装碎片。

文件内容必须依次覆盖以下五个层次，以自然段落形式书写，不使用 YAML 字段：

1. **角色定位** — 从 writing-style.yaml 的 role 取出，原样写入
2. **写作原则与禁忌** — 将 core_principles、possible_mistakes、depiction_techniques 三条的内容融合为自然段落，不要用列表。例如"你必须通过动作和微表情展示情绪，而不是直接说'他很愤怒'"
3. **故事背景** — 将 world-setting、角色当前状态、本卷冲突、场景时空融合为一段或两段叙述。让 subagent 读完就知道"这是一个什么世界、这些人是谁、此刻发生了什么"
4. **写作指引** — 即经 Phase 4 第一轮视角转换并经作者确认后的沉浸式内容。包含场景基调、关键节点、叙述约束
5. **写作要求** — 字数下限、节奏方向、结尾方向。用自然语言表达，如"本章不少于2000字，前松后紧，结尾不要总结"

文件和 example/ 下的示例提示词参考格式。

## 授权模式

- **步步授权（默认）**: 每步需作者确认
- **全部授权**: Agent 全权决定

作者可随时说"你全权决定"或"每步都要我确认"切换模式。

## Common Rationalizations

- "作者没回应我就继续往下走" → 必须等待确认
- "章纲差不多就行，不用那么详细" → 细节决定质量
- "角色设定差不多了，直接开始写" → 基础不牢地动山摇
- "提示词生成完不用给作者选了" → 作者选择权是核心流程
- "模板格式我看懂了，直接帮作者填好就行" → 禁止。Agent 只能引导讨论，不能代笔填充 YAML
- "作者说'写第一章'，我直接生成正文和所有相关文件" → 禁止。必须按 Phase 顺序逐阶段推进，每阶段确认后才产出文件
- "视角转换和变体一起生成，让作者一起看效率更高" → 禁止。视角转换必须先单独确认，确认后才能基于此生成变体。省一步就是省掉作者的控制权

## Red Flags

- 跳过 Phase 2 直接进入 Phase 3
- 不更新 story.yaml 就往下走
- subagent 生成正文时上下文不完整
- 正文写完不归档就直接结束
- 不更新角色 state_history
- 跳过 Phase 4 视角转换，直接用上帝视角章纲喂给 subagent
- Agent 未经作者讨论确认，直接参照模板格式自行填充 YAML 或生成正文
- 一次性产出多个 Phase 的文件（如同时创建 world-setting、character、volume、chapter）
- 作者说一句模糊指令（如"帮我写完"）就直接推进多个阶段
- 提示词采用 YAML 结构格式而非 prose——结构化碎片对 LLM subagent 效果打折，应使用自然段落
- 提示词缺失 writing-style 四个字段中的任何一个——缺少约束 subagent 必然放飞
- Phase 5 质量检查跳过 AI 味检测（anti-ai.yaml）——疲劳词和句式违规是读者流失的首要原因
- 归档时不更新 hooks.yaml——伏笔追踪断裂，长篇连续性崩溃
- 连续多章不检查 current-focus.md——故事方向漂移，角色行为失控

## 项目文件结构

初始化后的完整项目骨架：

```
project/
├── story.yaml                          # 项目索引
├── author-intent.md                    # 长周期作者意图
├── current-focus.md                    # 1-3章聚焦
├── settings/
│   ├── world-setting.yaml              # 世界设定
│   ├── writing-style.yaml              # 写作风格 + 题材配置 + 三层技法
│   ├── anti-ai.yaml                    # AI味检测规则
│   ├── hooks.yaml                      # 伏笔/钩子追踪
│   └── character-setting/              # 角色文件
├── volumes/                            # 卷文件
├── chapters/                           # 章纲
├── prompts/                            # 提示词（prose .md）
└── archives/                           # 正文
```

新增文件说明：

- **anti-ai.yaml**：中文/英文疲劳词 blocklist、句式规则、段落结构规则、对话规则、改写算法、严重度分级。Phase 5 正文质量检查的检测依据。
- **hooks.yaml**：伏笔全生命周期追踪（pending→mentioned→resolved→abandoned），支持 payoff_timing 调度、钩子操作语义（upsert/mention/resolve/defer/abandon）、陈旧度检测和收束健康检查。
- **author-intent.md**：作者长周期意图——核心主题、终局方向、写作信条、不妥协底线、长期伏笔池。
- **current-focus.md**：1-3章中周期聚焦——当前优先级、需推进支线、需提及钩子、节奏意图、限制约束。

## Verification

检查清单：
- [ ] 导入模式：已有正文已切分写入 archives/，设定已反向提取并经作者确认
- [ ] story.yaml 存在且包含正确的项目信息
- [ ] 每个设定阶段都有作者确认记录
- [ ] 题材配置已写入 writing-style.yaml 的 genre 字段
- [ ] hooks.yaml 已初始化，钩子操作语义作者已知晓
- [ ] 章纲包含所有必需字段 (summary, key_points, characters, location, time)
- [ ] 章纲讨论时同步更新了 hooks.yaml
- [ ] Phase 4 视角转换已完成且经作者确认
- [ ] 提示词为 prose 格式（非 YAML），包含五个层次：角色定位、写作原则与禁忌、故事背景、写作指引、写作要求
- [ ] 提示词已融入 writing-style 的 skill_layers（L1 结构层用于叙事约束、L2 内容层用于写作原则段、L3 审查层保留给 Phase 5 质量检查）
- [ ] 提示词中 writing-style 四个字段的内容已融入 prose——缺失任何一个 subagent 都会放飞
- [ ] 正文已通过 anti-ai.yaml 的六项质量检查（含 AI 疲劳词和句式违规检测）
- [ ] 正文已写入 archives/ 目录（Phase 5 落盘）后再进入归档流程
- [ ] 归档后的 markdown 命名正确 (vol-{N}-ch-{M}-{slugified-title}.md)
- [ ] 角色 state_history 在归档时更新
- [ ] hooks.yaml 在归档时更新（mention/resolve/defer），钩子健康检查已完成

