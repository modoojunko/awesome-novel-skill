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

- 用户说"写小说"、"创建小说项目"、"导入小说"
- 用户说"讨论世界设定"、"设计角色"
- 用户说"规划章节"、"写第X章"
- 用户说"生成正文"、"继续写"

**When NOT to use:** 用户只是想聊小说内容、不需要系统化工作流。

## Process

### Phase 1: Init - 创建项目

触发条件：用户说"写小说"、"创建小说项目"、"导入小说"、"续写已有小说"

Agent 首先判断用户意图——是新建还是导入：

**情况 A：新建小说**

1. 执行 `python scripts/init.py [项目名] [--author 作者名]`
2. 询问作者 title 和 author（若未通过 --author 传入）
3. 将 title、author、created_at 写入 story.yaml
4. 提示作者进入项目目录，写作风格指南已预填默认设定，进入 Phase 2

**情况 B：导入已有小说**

1. 执行 `python scripts/init.py [项目名] [--author 作者名]`
2. 请作者提供已有小说文件（支持 .txt / .md，单文件或多文件）
3. 执行 `python scripts/import.py [项目路径] [小说文件]` 自动切分章节、写入 archives/ 和 chapters/
4. Agent 逐章阅读正文，反向提取以下信息：
   - **世界设定**：推断世界观类型、地理、社会规则等 → `settings/world-setting.yaml`
   - **角色设定**：识别出场角色，提取认知方式、价值观、能力等维度 → `settings/character-setting/`
   - **写作风格**：分析叙事习惯（用词偏好、句式特征、对话风格）→ `settings/writing-style.yaml`
   - **钩子追踪**：识别已有伏笔和未解决线索 → `settings/hooks.yaml`
5. 根据已有正文反写各章的 outline 字段
6. 创建 `volumes/volume-N.yaml` 卷纲
7. 更新 `story.yaml` 索引
8. 反向提取完成后，执行 `python scripts/check_completeness.py [项目路径]` 扫描空字段，然后 Agent 输出 **导入完整性报告**：

   | 文件 | 字段 | 状态 | 影响 |
   |------|------|------|------|
   | world-setting.yaml | geography | ✅ 已提取 | — |
   | world-setting.yaml | politics | ⚠️ 已推测 | Phase 4 提示词可能缺少政治背景 |
   | world-setting.yaml | history | ❌ 未找到 | Phase 4 提示词无历史语境 |
   | character-setting/xx | cognition | ❌ 未找到 | 角色行为可能不一致 |
   | hooks.yaml | — | ✅ 3个钩子 | — |
   | writing-style.yaml | depiction_techniques | ✅ 已分析 | — |

   每个 ❌/⚠️ 项附带一句说明：这个缺失在实践中意味着什么，作者是否需要在进入 Phase 4 前补充。

9. **STOP：将完整性报告展示给作者。** 作者决定：
   - "就这样，缺的后面再说" → 进入 Phase 4，Agent 写作时对缺失字段不做假设
   - "先补几项" → Agent 逐项引导补充
   - "缺太多，走完整设定流程" → 转入 Phase 2 从头讨论

10. 确认当前进度后，后续从 Phase 4 开始继续创作

### Phase 2: 设定阶段 - 世界 & 角色 & 写作风格

触发条件：Phase 1 新建模式完成，作者说开始设定

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

author-intent.md 填写（Phase 2 最后一步）:
1. 此时世界设定、角色设定、写作风格、题材、钩子均已确认，作者对故事的全局方向已有完整认知
2. Agent 引导作者填写 `author-intent.md`：核心主题、终局方向、写作信条、绝不妥协、长期伏笔池
3. 如果作者暂时不想确定终局，至少填写"核心主题"和"写作信条"——这两条直接影响 Phase 4 提示词的写作指引段
4. **STOP：作者确认后再进入 Phase 3**

### Phase 3: 故事线拆分 + 卷纲 + 章纲

触发条件：用户确认设定阶段完成

**Phase 3 前置检查（必须执行，不可跳过）**：

Agent 必须先读取 `author-intent.md` 和 `current-focus.md`，检查是否为模板默认内容（未修改过），然后向作者报告：

> author-intent.md：核心主题已有 / 仍是模板，建议填入后再规划章节。current-focus.md：1-3 章聚焦已有 / 仍是模板。

如果两个文件仍是模板默认内容，**STOP——先问作者是否需要填写，确认后再开始讨论章纲。** 跳过此检查会导致 Phase 4 写作指引缺少作者意图约束，subagent 生成的方向可能与作者期望偏离。

流程（以卷1为例）:
1. 创建 `volumes/volume-1.yaml`，写入卷标题和卷概要
2. 讨论卷纲：本卷核心冲突、主要事件、角色弧光走向
3. 将章节摘要列表写入 volume-1.yaml 的 chapters_summary
4. 逐章讨论章纲 → 创建 `chapters/vol-1-ch-1.yaml`
   a. 先讨论 plot outline（剧情要点），确认后填入 outline 字段
   a2. outline 确认后，**必须询问作者**："本章有没有明确禁止出现的场景、元素或情节？有没有绝对不能写的东西？" 将作者回答记录到 memo.prohibitions。如果作者说"没有"，也要确认一次——有时作者事后才想起来。
   b. 再讨论 chapter memo（读者情绪设计），分为 7 段：
      - **当前任务**：本章必须完成的具体动作（对齐卷纲节点）
      - **读者此刻在等什么**：上一章结束时读者的情绪状态 + 本章策略（制造新缺口/延迟兑现/兑现旧缺口/双重）
      - **该兑现的 / 暂不掀的**：确认哪些伏笔必须兑现、哪些必须压住
      - **日常/过渡承担什么任务**：非冲突段落的功能映射（埋伏笔/推关系/建反差/信息铺垫/情绪缓冲）
      - **关键抉择过三连问**：关键选择的检验（为什么/符合人设吗/读者觉得突兀吗）
      - **章尾必须发生的改变**：1-3 条具体改变（信息/关系/物理/权力）
      - **不要做**：本章硬约束红线
     c. 填写 emotional_design 字段（主情绪基调、情绪走向、强度峰值、爽点位置、章尾钩子类型、整体强度1-10）
     d. 同步讨论本章的钩子操作：
        - 本章是否埋下新伏笔？（upsert）→ 如果埋新伏笔，Agent 在本章正文归档时从正文中提取 1-3 句原文填入 hooks.yaml 的 seed_text 字段
        - 本章是否提及/推进已有伏笔？（mention）
        - 本章是否收束某个伏笔？（resolve）→ 如果要收束，Agent 在 Phase 4 视角转换时必须将该钩子的 seed_text（种下时的原文片段）注入写作指引段，让 subagent 接着读者已经看到的画面来写兑现
     e. 更新 settings/hooks.yaml 中受影响的钩子条目
     f. 确认本章的微兑现（micro_payoffs）设计：本章读者至少能"获得"什么？从以下 7 种中选择至少 1 种，填入 emotional_design.micro_payoffs：
        - **信息兑现**：新线索/新信息（读者知道了之前不知道的事）
        - **关系兑现**：关系推进/接触（角色间的距离发生了变化）
        - **情绪兑现**：情绪释放/共鸣（读者感到爽、暖、释然或被触动）
        - **线索兑现**：伏笔回收/推进（之前的某个伏笔在本章有进展）
        - **能力兑现**：能力提升/新技能（角色变强了或获得了新工具）
        - **资源兑现**：获得物品/资源（角色得到了什么）
        - **认可兑现**：获得认可/面子（角色被他人承认或尊重）
        Agent 参考 writing-style.yaml > genre.retention_config 的 micropayoff_min_per_chapter，检查本章微兑现数是否达标。过渡章也必须至少 1 个微兑现。如果本章没有任何微兑现——警告作者：读者看完会觉得"这章什么都没得到"。
5. 重复直到本卷所有章纲完成
6. 更新 story.yaml 的 volumes 和 chapters 列表
7. 进入下一卷，直到本卷规划完成

current-focus.md 填写（Phase 3 最后一步）:
1. 章纲规划完成后，Agent 引导作者填写 `current-focus.md`
2. 填入接下来的 1-3 章聚焦：当前优先级、需推进的支线、需提及的钩子、节奏意图、限制约束
3. 这份内容将直接进入 Phase 4 视角转换的写作指引段——它是章纲和正文之间最直接的"作者意图→写作约束"桥梁
4. **STOP：作者确认后再进入 Phase 4**

### 控制文档（可选，随时更新）

项目根目录下的 `author-intent.md` 和 `current-focus.md` 是作者直接表达意图的轻量级文档，不经过 YAML 结构化。

- **author-intent.md**：长周期方向。核心主题、终局设想、写作信条、绝不妥协的底线、长期伏笔池。Agent 在每次 Phase 3 章纲讨论和 Phase 4 视角转换时都应读取此文件。
- **current-focus.md**：接下来 1-3 章的聚焦。当前优先级、需推进的支线、需提及的钩子、节奏意图、限制约束。Agent 在 Phase 3 章纲讨论和 Phase 4 第一轮视角转换时必须读取此文件。

作者可以随时说"更新作者意图"或"更新当前聚焦"来修改这两个文件。Agent 应主动引导作者在每写完 3-5 章后审视并更新 current-focus.md。

章纲内容（chapter.yaml 字段）:
- outline.summary: 本章核心情节点
- outline.key_points: 本章要点列表
- outline.characters: 本章涉及的角色列表（引用角色 yaml 文件名）
- outline.location: 场景地点（**禁止使用编号代号**如"烧烤摊A/B/C"，必须用具体有特色的名称）
- outline.time: 时间背景
- outline.summary 和 key_points 中的场景/道具名称也必须具体化，禁止出现"道具A""路人甲"等代号——这些代号会被 subagent 照搬进正文
- memo.current_task: 本章必须完成的具体动作
- memo.reader_expectation: 读者此刻在等什么 + 本章情绪策略
- memo.payoff_plan: 该兑现/暂不掀的伏笔管理
- memo.downtime_functions: 日常/过渡段落的功能映射
- memo.key_choices: 关键抉择的三连问检验
- memo.required_changes: 章尾必须发生的 1-3 条具体改变
- memo.prohibitions: 本章硬约束红线
- emotional_design.primary_mood: 本章主情绪基调
- emotional_design.mood_progression: 情绪走向（从→经过→以…结束）
- emotional_design.intensity_level: 整体情绪强度 (1-10)
- emotional_design.emotional_hook: 章尾情绪钩子类型

章状态（chapter.status）:
- `outline` — 章纲和情绪设计已确认，等待生成提示词
- `draft` — 提示词已生成，正文写作/修改中，等待归档
- `archived` — 正文已归档

卷与章的关系以 story.yaml 的 chapters 列表为唯一数据源，volume.yaml 的 chapters_summary 仅作为规划阶段的摘要参考。

### Phase 4: 提示词生成

触发条件：章状态为 outline 且章纲获作者确认

**Phase 4 前置检查（必须执行，不可跳过）**：

Agent 必须重新读取 `author-intent.md` 和 `current-focus.md`，确认内容与章纲一致，然后向作者报告：

> author-intent.md：本章与核心主题一致 / 存在偏离。current-focus.md：本章在 1-3 章优先级范围内 / 偏离当前聚焦。

如果存在偏离，**STOP——先与作者讨论是否调整章纲或更新控制文档。** 跳过此检查会导致视角转换缺少方向约束，提示词变体可能跑偏。

本阶段分两轮进行，每轮必须等作者确认后才能进入下一步。**严禁在作者确认视角转换前提前生成提示词变体。**

**第一轮：视角转换**

1. 读取章纲 `chapters/vol-N-ch-M.yaml` 的 outline 字段
2. 按视角转换规则（见下方）将上帝视角章纲转换为沉浸式写作指引
3. **STOP：将转换后的内容展示给作者，等待确认。作者不满意则继续调整，直到确认。**
4. 作者确认视角转换后，进入第二轮。

**第二轮：组装提示词并生成变体**

5. **必须先读取 `settings/writing-style.yaml` 的全部字段**，按以下聚合清单逐项处理。**全部字段聚合完毕后才能进入步骤 6。缺失任何一个字段 subagent 都会缺少对应约束。**

   **聚合清单（逐项执行，每完成一项在脑内确认）**：

   | # | 字段 | 融入目标段 | 关键内容 |
   |---|------|-----------|---------|
   | 1 | `role` | 角色定位段 | 原样写入 |
   | 2 | `core_principles` | 写作原则与禁忌段 🔴 | 全局规则、自然表达、描写替代描述、角色构建 |
   | 3 | `possible_mistakes` | 写作原则与禁忌段 🔴 | 常见错误清单，转为禁止语句 |
   | 4 | `depiction_techniques` | 写作原则与禁忌段 🟡 | 五种描写技法（动作/对话/微表情/环境互动/内心独白） |
   | 5 | `reader_psychology` | 写作原则与禁忌段 🟡 | 期待管理、信息落差、情绪节拍、锚定效应、沉没成本 |
   | 6 | `emotional_pacing` | 写作原则与禁忌段 🟡 | 关系递进规则、情绪升级法 |
   | 7 | `creative_constitution` | 写作原则与禁忌段 🟡 | 14 条写作脊梁，转为自然段落约束 |
   | 8 | `character_psychology_method` | 写作原则与禁忌段 🟡 | 六步推导法——subagent 写关键场景前必须先推导角色行为 |
   | 9 | `desire_engine` | 写作要求段 | 基础欲望 + 主动欲望，告诉 subagent 本章要满足读者的什么欲望 |
   | 10 | `immersion_pillars` | 写作要求段 | 六支柱作为场景设计默认模板 |
   | 11 | `genre` | 写作原则与禁忌段 🟡 + 写作要求段 | 爽点类型/节奏红线→写作要求段；反套路规则→写作原则段 |
   | 12 | `skill_layers` | L1→视角转换 / L2→写作原则段 / L3→Phase 5 保留 | 三层各司其职，不全部塞给 subagent |

   **聚合完毕后自检**：逐项确认以上 12 项是否都已出现在提示词中。如有任何一项未聚合，**STOP**——补全后再继续。
   - **约束优先级分层**：将上述所有约束按三级标注，写入提示词"写作原则与禁忌"段时物理分离：
     - 🔴 **硬禁止（Hard Prohibition）**：违反即不合格。包括：禁止"他感到/他觉得/他意识到"、禁止元叙事、禁止文末总结升华、禁止俗套比喻、禁止副词修饰对话标签、禁止"不是……而是……"句式（单章不超过 3 次）。写入提示词时放在最前面，以"以下行为绝对禁止，违反任何一条正文即为不合格"领起。
     - 🟡 **强建议（Strong Recommendation）**：应该遵守，偶有违反可容忍。包括：五感锚定、对话即动作、Show Don't Tell、期待管理、情绪节拍、欲望驱动。写入提示词时放在🔴之后，以"以下原则必须遵守"领起。
     - 🟢 **软引导（Soft Guidance）**：尽力而为，不影响合格判定。包括：句式变化、成语密度、段落节奏。写入提示词时放在最后，以"以下技法请注意"领起。
     - 🔴和🟡之间空一行，🟡和🟢之间空一行——物理分隔让 subagent 不可能把硬禁止和软建议混为一谈。
6. 读取其余源文件，按映射表将各来源内容转为自然段落
7. 将第一轮确认后的沉浸式内容作为"写作指引"段写入
8. **生成 PRE_WRITE_CHECK 写作执行清单**：主 Agent 根据本章的 memo + emotional_design + cycle_position + micro_payoffs，生成一份"写作执行清单"（见下方格式），列出 subagent 动笔前必须对齐的所有约束。清单以 prose 段落形式写入提示词文件的"写作执行清单"段——不是 markdown 表格，是自然段落指令。内容必须覆盖：
   - 当前任务与执行动作（从 memo.current_task）
   - 读者情绪处理策略（从 memo.reader_expectation）
   - 伏笔兑现/压住清单（从 memo.payoff_plan）
   - 章尾必须发生的改变（从 memo.required_changes）
   - 本章微兑现要求（从 emotional_design.micro_payoffs）
   - 爽感循环位置与策略（从 emotional_design.cycle_position + suppression_stack / release_target）
   - 不要做的红线（从 memo.prohibitions）
9. 基于同一 content + PRE_WRITE_CHECK 清单，生成 3 个提示词变体（不同切入角度/叙事策略，每个变体均包含该清单作为"写作执行清单"段）
10. **STOP：将 3 个变体展示给作者选择（含 PRE_WRITE_CHECK 清单），作者不满意则调整，直到确认。**
11. 作者确认后，将章节状态从 outline → draft
12. 确保 `prompts/` 目录存在，保存为 `prompts/vol-N-ch-M-prompt.md`

**提示词组装映射表**（源文件 → 提示词 prose 段落）:

| 读取的源文件 | 映射到提示词字段 | 说明 |
|-------------|-----------------|------|
| writing-style.yaml > role | 角色定位段 | 原样写入 |
| writing-style.yaml > core_principles + possible_mistakes + depiction_techniques + reader_psychology + emotional_pacing + creative_constitution + character_psychology_method | 写作原则与禁忌段 | 融合为自然段落（期待管理、信息落差、情绪节拍、欲望驱动、情感节点设计、创作宪法全部融入） |
| writing-style.yaml > desire_engine + immersion_pillars | 写作要求段 | 本章的情绪回报目标和场景设计模板 |
| world-setting.yaml > details | 故事背景段 | 融合为叙述 |
| character-setting/[角色].yaml | 故事背景段 | 角色当前状态，融入背景叙述 |
| volume-N.yaml | 故事背景段 | 本卷冲突、主线，融入背景叙述 |
| chapter.yaml > outline.location + time | 场景段 | 场景时空 |
| chapter.yaml > outline | 写作指引段 | 章纲经视角转换后填入（见下方规则） |
| chapter.yaml > memo + emotional_design | 写作指引段 | 读者情绪设计融入视角转换——"读者此刻在等什么"、"章尾必须发生的改变"、"情绪基调与强度"作为视角转换的核心约束 |
| hooks.yaml > 待兑现/推进钩子的 seed_text | 写作指引段 | 在有钩子需要兑现或推进的章节，将种下时的原文片段注入写作指引，让 subagent 接着读者已经看到的画面来写兑现——不是"揭晓真相"，而是"读者在第X章看到的那个画面，现在有了后续" |
| hooks.yaml > 钩子的 hook_strength + hook_position | 写作指引段 | 告诉 subagent 本章的钩子应该多强（strong/medium/weak）以及放在章内还是章末 |
| chapter.yaml > emotional_design.micro_payoffs | 写作要求段 | 告诉 subagent 本章读者至少要获得什么——"本章必须让读者至少得到[具体的微兑现内容]，如果没有，这一章就不算完成" |

**视角转换规则**（章纲 → 提示词 content 字段）——一句话概括：

> **把"发生了什么事"重写为"事情发生时，在场的人感受到了什么"——前者是给作者看的，后者才是给 subagent 写的。**

转换要求：
- 禁止在 content 中出现"本章讲述了""主角经历了""剧情推进到"等上帝视角概述语
- 将章纲的事件概要改写为场景化指引：从谁的视角出发、看到了什么、感受到了什么、发生了什么冲突
- 用具体可感的细节替代抽象总结，比如"两人决裂"应变为"对话中逐渐积累的误解在某个瞬间爆发，两人各自的选择将关系推向不可挽回的方向"
- content 应是"让作者沉浸到场景中去写"的指引，而非"告诉 subagent 剧情是什么"的摘要
- **指引不是剧本。禁止按时间顺序逐段描述'先写什么再写什么'。给出氛围基调、关键情节点、情感走向即可，把具体的叙事节奏、细节选择和语言组织留给 subagent。如果 content 读起来像分镜脚本，说明粒度太细了。**
- 禁止自由发挥联想，严格基于章纲已确认的情节，仅改变叙述视角，不添加章纲中没有的事件

**钩子兑现锚定规则**：如果本章 memo.payoff_plan.must_resolve 或 partial_advance 中有钩子需要兑现或推进，视角转换时必须将该钩子的 seed_text（种下时的原文片段）嵌入写作指引段。格式参考："> 读者在第 X 章看到过：'[seed_text 原文引用]'——本章需要接着这个画面来写兑现/推进。不是轻描淡写一句话带过，而是让读者感觉到'这个坑终于填了'——兑现段落应在情绪或画面上与原文片段形成呼应。"

**爽感循环感知规则**：视角转换时必须读取 chapter.yaml 的 emotional_design.cycle_position，根据位置注入不同的叙事指令：

> **压制章（suppression_N）**：视角转换后的写作指引必须包含——(a) 本章积累的"债"是什么（谁对主角做了什么，读者为什么该感到愤怒/不公/心疼），必须写成一个让读者想替主角出头的具体瞬间，禁止写成"主角很惨"的概括；(b) 前面已经积累了哪些压制（引用前面压制章的编号和 suppression_stack 内容），本章的压制如何比上一轮更过分——不是同一种压制重复，是换个角度/施压方/代价；(c) 章尾暗示——不是"主角会赢"的剧透，是"再忍一下，快了"的预感。
>
> **释放章（release）**：视角转换后的写作指引必须包含——(a) 本章要兑现前面哪些压制章的债，逐条对应，引用前面压制章编号和 specific 债的内容；(b) 每个债的兑现方式——怎么打回去的、为什么比读者预期的更过分。反派的表情必须从不在乎→开始慌→彻底崩溃，旁观者反应必须从震惊→后悔看走眼→立即倒戈，主角姿态是从容不迫（不是嚣张——他早就知道会这样）；(c) 余波——释放之后谁失去了什么、谁得到了什么、关系怎么变了。必须引用前面压制章的 seed_text 或关键场景，让兑现与压制在画面或情绪上形成呼应。
>
> **余波章（aftermath）**：视角转换后的写作指引必须包含——(a) 上一轮释放后世界发生了什么变化（谁的态度变了、什么规则被改写了、主角获得了什么新东西）；(b) 在平静中埋下新一轮压制的种子——下一个更大的威胁是什么，让读者隐约感到"更大的还在后面"。

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
  prompt: "读取 prompts/vol-{N}-ch-{M}-prompt.md。该文件是你的完整写作指令，从角色定位到场景细节到字数要求到读者情绪设计全部包含在内。

严格按文件中的所有要求写作：
1. 文件中已包含写作风格约束、常见错误清单、描写技法指南、读者心理学框架（期待管理、信息落差、情绪节拍、欲望驱动）——每一条都必须遵守。
2. 文件中已包含场景基调、关键节点、叙述约束、读者情绪设计（本章要让读者感受到什么情绪、章尾要留下什么情绪缺口）和写作要求。**写作要求中的字数下限为硬性指标。正文完成后必须自行统计字数：若不足要求下限，视为不合格，需重新生成。不允许多次生成仍不达标的情况——如果第一次不足，第二次必须补足。**
3. 写作时同步考虑读者的心理状态：
   - 读者此刻在等什么？如果是等兑现——在本章给足；如果是等揭晓——先给半个答案再关上门
   - 情绪节拍：压制→释放→更大的压制→更大的释放。释放时超过读者的心理预期。只满足70%的期待等于失败
   - 章尾必须留下情绪缺口——悬念、共情、期待三者至少占一样
   - 坏事叠坏事升级：不是一次到位，而是层层加码，每层比上一层更过分
   - 如果要兑现/推进伏笔，必须接着提示词文件中提供的原始画面来写——不是'揭晓真相'，而是'读者在第X章看到的那个画面，现在有了后续'。兑现场景在情绪或画面上应与原文片段形成呼应
   - 爽感循环感知——提示词文件中已标明本章在压制→释放周期中的位置，必须按对应策略写作：
     * 如果本章是压制章：不要写"主角很惨"的概括。写具体的、让读者感到不公/愤怒/心疼的瞬间。每一层压制都是读者脑子里的一笔"债"，他们等着你还。压制必须比上一轮更过分——同一种压制用两次，读者会觉得你在拖
     * 如果本章是释放章：还债的时刻。赢了不够——要赢得比读者预想的更过分。反派表情必须从不在乎→发慌→彻底崩溃。旁观者必须有反应——后悔当初看走眼的、立刻倒戈的、不敢置信的。主角姿态是从容不迫，不是嚣张——他早就知道会这样。释放后要有余波：谁失去了什么、谁得到了什么
4. 提示词文件中已包含"写作执行清单"（PRE_WRITE_CHECK），列出了本章的所有执行约束——当前任务、读者情绪处理策略、伏笔兑现/压住清单、章尾必须发生的改变、微兑现要求、爽感循环位置、不要做的红线。严格对照这份清单写作，每条都必须体现在正文中。
5. 禁止以下句式和行为：
   - 禁止'他感到''他觉得''他意识到'等直接描述情绪或认知的句式——用身体反应、动作、环境互动替代
   - 禁止'本章讲述了''接下来'等元叙事语句
   - 禁止在文末进行任何总结、升华、点评
   - 禁止使用俗套比喻
   - 禁止用副词修饰对话（如'她愤怒地说'），对话本身传达情绪
   - 禁止过度使用'不是X，而是Y'对比句式——单章不超过 3 次。这不是写作风格，是 LLM 统计癖好。如果需要对比，用两个独立句子替代
6. 只输出正文本身。输出中禁止出现任何解释、说明、注释、前缀、后缀、'以下是正文'或类似引导语。从第一个字开始就是小说正文，最后一个字结束就是小说结束。"
)
```

**放弃 subagent 输出的判断标准**：

subagent 返回的正文在展示给作者之前，主 Agent 必须先检查以下十一项（含 AI 味检测、情绪缺口检测、跨章情绪单调检测、微兑现检测、安全着陆检测）。**任意一项触发，不展示正文，向作者报告具体问题，由作者决定下一步：重新调用 subagent、主 Agent 按指令重写、或作者给出方向后主 Agent 修改。**

检测时参考 `settings/anti-ai.yaml` 中的 fatigue_words、sentence_rules、paragraph_rules、dialogue_rules、emotional_cadence、stagnation、safe_landing 七个规则组。

| 触发条件 | 报告内容 |
|---------|---------|
| 字数不达标 | 告知作者：实际字数 vs 要求字数下限，询问是否接受当前长度还是重写 |
| 上帝视角摘要 | 摘出正文中典型的概述句式（如"他经历了""本章讲述了"），向作者说明为什么这些段落读起来像梗概而非叙事，询问是否按提示词要求重写 |
| 违反核心约束 | 指出正文中违反的具体约束条款（引用提示词文件中的禁止条目），说明违规位置 |
| 夹带非正文内容 | 指出正文前后的引导语、解释、或文末的总结升华段落 |
| AI疲劳词触发 | 对照 `settings/anti-ai.yaml` 的 fatigue_words 列表扫描正文，统计高频疲劳词出现次数和位置，向作者报告风险等级（严重/高/中/低）。严重级（元叙事、上帝视角词）必须重写。 |
| AI句式违规 | 检测连续同结构开头、列表式叙述、说明书式对话，向作者报告违规位置和建议改法 |
| **结构性句式癖好触发** | 对照 `settings/anti-ai.yaml` 的 structural_tic_patterns 列表，用 grep 正则扫描正文。统计每种模式的命中次数，超过阈值的向作者报告模式名称、命中次数和阈值。例如"不是……而是……"句式单章出现 8 次（阈值 3），报告：该句式过多导致叙述节奏单一，建议分散到不同句式或直接删减 |
| **章尾情绪缺口检测** | 本章结尾是否留下了读者"想知道接下来会怎样"的钩子？没有则标记为"缺钩子——读者没有继续阅读的理由"。检查章尾 200 字是否满足 chapter.yaml 的 emotional_design.emotional_hook 指定的钩子类型（悬念/共情/期待/愤怒/好奇） |
| **情绪兑现检测** | 对照 chapter.yaml 的 memo.reader_expectation：如果策略是"兑现旧缺口"，检查正文中是否确实有兑现段落；如果策略是"制造新缺口"，检查正文结尾是否留下了新的"读者想知道"的问题 |
| **跨章情绪单调检测** | 读取 `settings/anti-ai.yaml` 的 emotional_cadence 规则组：检查最近 3-5 章的主情绪基调是否连续相同（连续高压/连续平淡），是否连续使用同一种章尾钩子类型。如果检测到单调性，向作者报告并建议调整 |
| **微兑现缺失** | 对照 chapter.yaml 的 emotional_design.micro_payoffs：本章是否至少有一处让读者感到"有收获"的段落？过渡章是否也达到最低要求（参考 writing-style.yaml > genre.retention_config.micropayoff_transition_min）？如果本章没有任何微兑现，标记为"微兑现缺失——读者看完会觉得这章什么都没得到" |
| **安全着陆检测** | 读取 `settings/anti-ai.yaml` 的 emotional_cadence.safe_landing：本章结尾是否所有冲突都被解决、没有任何未闭合的问题？如果是，标记为"安全着陆——章尾没有留给读者任何悬念或情绪缺口，读者没有点下一章的理由"。注意区分"自然收束"和"安全着陆"——前者允许有遗留问题，后者是所有冲突完美解决 |
| **物品/状态一致性** | 检查正文中物品的归属、状态变化是否合理。关键检查点：(1) 物品是否已被消耗但后文仍在使用（如"矿泉水瓶灌了两口放下"后文不应出现"手里的矿泉水瓶"）；(2) 物品来源是否与前文一致（是否突然出现未经交代的物品）；(3) 角色携带物品在场景切换时是否合理（丢失/获得是否有交代）。发现不一致则报告具体位置和矛盾内容 |

**结构性句式癖好检测方法**：subagent 返回正文后，主 Agent 使用 Bash 执行 grep 正则扫描。以"不是而是"句式为例：

```bash
# 统计 "不是X而是Y" / "不是X，是Y" 句式出现次数
grep -cP '不是.{1,20}(而是|，是|,是)' archives/vol-00N-ch-00M-*.md
```

对照 `anti-ai.yaml` 的 `structural_tic_patterns` 中每个模式的 threshold。超阈值则在质量报告中列出：模式名称、命中次数、阈值、建议操作。

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
5. 分析并记录本章情绪数据：
   - 对照 chapter.yaml 的 emotional_design，验证正文实际达到的情绪效果是否与设计一致
   - 为每个出场角色追记情感弧线条目（见下方 emotional_arc 格式），包含情绪状态、触发事件、强度(1-10)、弧线方向
   - 更新 anti-ai.yaml 的 emotional_cadence 相关统计（最近章的 primary_mood 序列用于跨章单调检测）
6. 更新 hooks.yaml：检查本章内容中是否有钩子被提及、推进或收束，执行对应操作（mention/resolve/defer），更新 last_mentioned_chapter 和 status 字段
7. 运行钩子健康检查（参考 hooks.yaml 的 hook_health_rules）：
   - 是否有超过陈旧阈值的高优先级钩子？
   - 是否有本章集中收束超过 3 个钩子的情况？
   - 钩子强度分布是否健康（连续 weak 不超过 3 章，每 5 章至少一个 strong）？
   - 将检查结果报告给作者
8. 运行情节推进停滞检测（参考 anti-ai.yaml 的 emotional_cadence.stagnation）：
   - 检查最近 N 章（默认 3 章）：是否每章至少有"新信息/关系变化/能力状态变化/伏笔推进/冲突升级"中的一项？
   - 如果连续 N 章无任何推进 → 触发 HARD-003 停滞警告，向作者报告："最近 N 章无实质性推进，读者可能感到节奏停滞"
   - 如果本章无任何冲突/问题/目标 → 触发 HARD-004 冲突真空警告："本章没有需要解决的问题，读者无法回答'这章要解决什么'"
9. 将 chapter.yaml 的 status 更新为 `archived`
10. 更新 story.yaml 的 chapters 列表中对应条目
11. **滑动窗口审视 current-focus.md**（每章归档后必做，不可跳过）：
    - 读取 `current-focus.md`，检查其中的"当前优先级"和"节奏意图"是否仍然适用
    - 将刚归档的章节标记为 ✅（已完成）
    - 以最近 3 章为滑动窗口，判断：(a) 优先级是否需要调整——是否有支线已收束、新支线已展开；(b) 节奏意图是否偏移——连续 3 章的 primary_mood 是否偏离了 current-focus.md 设定的方向；(c) 需提及的钩子是否已处理——已兑现的移除、新增的加入
    - 如果窗口内的章节状态与 current-focus.md 记录不符，**向作者报告差异并建议更新**。作者确认后写入。如果无需更新，向作者报告"滑动窗口内状态一致，current-focus.md 无需更新"
    - 特别关注：每 3 章的倍数节点（第 3、6、9…章归档后），**必须引导作者**重新审视并主动更新 current-focus.md，而非仅做被动检查

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

角色 emotional_arc 格式（追加到 character yaml 的 emotional_arc 数组末尾）:
```yaml
emotional_arc:
  - volume: 1
    chapter: 1
    emotional_state: "本章角色情绪状态（愤怒/压抑/释然/期待/恐惧/温情/决心）"
    trigger_event: "触发该情绪的具体事件"
    intensity: 7          # 情绪强度 1-10
    arc_direction: ""     # 弧线方向：rising（上升）/ falling（下降）/ holding（维持）/ turning（转折）
    expression: ""        # 情绪如何外化（身体反应/行为/对话/环境互动）
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

文件内容必须依次覆盖以下六个层次，以自然段落形式书写，不使用 YAML 字段：

1. **角色定位** — 从 writing-style.yaml 的 role 取出，原样写入
2. **写作原则与禁忌** — 将 core_principles、possible_mistakes、depiction_techniques、reader_psychology、emotional_pacing、creative_constitution、character_psychology_method 融合为自然段落，但必须按三级优先级物理分离：
   - 🔴 **硬禁止（违反即不合格）**：禁止"他感到/他觉得/他意识到"、禁止元叙事、禁止文末总结升华、禁止俗套比喻、禁止副词修饰对话标签、禁止"不是……而是……"句式（单章不超过 3 次）。以"以下行为绝对禁止，违反任何一条正文即为不合格"领起。
   - 🟡 **强建议（必须遵守）**：五感锚定、对话即动作、Show Don't Tell、期待管理、情绪节拍、欲望驱动。以"以下原则必须遵守"领起。
   - 🟢 **软引导（请注意）**：句式变化、成语密度、段落节奏。以"以下技法请注意"领起。
   - 三段之间空一行物理分隔。禁止将🔴硬禁止淹没在🟡🟢的段落中——subagent 只会记住段首和段尾，埋在中段的约束等于不存在。
3. **故事背景** — 将 world-setting、角色当前状态、本卷冲突、场景时空融合为一段或两段叙述。让 subagent 读完就知道"这是一个什么世界、这些人是谁、此刻发生了什么"
4. **写作指引** — 即经 Phase 4 第一轮视角转换并经作者确认后的沉浸式内容。包含场景基调、关键节点、叙述约束、爽感循环策略、钩子兑现锚定
5. **写作执行清单** — 主 Agent 在 Phase 4 步骤 8 生成的 PRE_WRITE_CHECK 清单，以 prose 自然段落形式告诉 subagent：本章必须完成什么动作、读者此刻在等什么、必须兑现/压住的伏笔清单、章尾必须发生的改变、本章微兑现要求、爽感循环位置与策略、不要做的红线
6. **写作要求** — 字数下限（不少于3000字）、节奏方向、结尾方向、欲望引擎和代入感支柱。用自然语言表达，如"本章不少于3000字，前松后紧，结尾不要总结"

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
- "章纲的 memo（读者情绪设计）可以跳过，直接进入视角转换" → 禁止。memo 是视角转换的约束来源——"读者此刻在等什么"决定了叙事策略。没有 memo 的视角转换等于没有罗盘的航行
- "emotional_design 的 primary_mood 随便写一个就行" → 禁止。情绪基调决定了整章的节奏和叙事策略。连续章的情绪基调决定长篇的读者疲劳度
- "硬禁止和软建议写一起就行了，subagent 能区分" → 禁止。LLM 对段首和段尾的记忆权重最高，埋在段落中间的硬禁止等同于不存在。必须🔴🟡🟢三层物理分离，硬禁止单独成段在第一位

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
- Phase 3 或 Phase 4 跳过 author-intent.md / current-focus.md 前置检查——这两个文件是"作者意图→Agent 执行"的唯一桥梁，跳过等于让 subagent 在没有方向约束的情况下自行判断故事走向
- Phase 3 章纲讨论跳过 memo（读者情绪设计）——子智能体只知剧情不知情绪，正文必然缺少情绪调动
- Phase 4 视角转换未融入 chapter.yaml 的 emotional_design——提示词缺少情绪约束，subagent 自由发挥导致情绪走偏
- Phase 5 质量检查跳过章尾情绪缺口检测——章节结尾没有钩子，读者流失风险被忽视
- Phase 6 归档不记录 emotional_arc——跨章情绪追踪断裂，长篇情绪节奏失控
- 连续 3 章以上 primary_mood 相同——情绪单调导致读者疲劳，应在章纲阶段调整节奏
- 连续 3 章以上无任何微兑现——读者累积"什么都没得到"的挫败感，留存崩盘
- 章尾安全着陆（所有冲突完美解决）——读者没有点下一章的理由
- Phase 3 章纲讨论跳过微兑现设计——subagent 不知道本章要给读者什么收获，正文必然缺乏即时满足
- 提示词"写作原则与禁忌"段不按🔴🟡🟢三层物理分离——硬禁止淹没在软建议中，subagent 把"绝对禁止"当"建议参考"，约束形同虚设
- Phase 5 跳过结构性句式癖好检测——"不是而是"等 LLM 统计癖好不被发现，每章累积 5-10 次，读者在 10 章内感知到"机器味"并流失

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
- [ ] 章纲包含所有必需字段 (outline + memo + emotional_design)
- [ ] 章纲讨论时同步更新了 hooks.yaml
- [ ] Phase 3 chapter memo 的 7 段（尤其是"读者此刻在等什么"和"章尾必须发生的改变"）已经作者讨论确认
- [ ] Phase 4 视角转换已完成且经作者确认
- [ ] 提示词为 prose 格式（非 YAML），包含六个层次：角色定位、写作原则与禁忌、故事背景、写作指引、写作执行清单、写作要求
- [ ] 提示词"写作原则与禁忌"段已按🔴🟡🟢三层物理分离，硬禁止在最前面单独成段
- [ ] 提示词已融入 writing-style 的 reader_psychology、desire_engine、immersion_pillars、emotional_pacing、creative_constitution、character_psychology_method（融入写作原则段和写作要求段）
- [ ] 提示词已融入 chapter.yaml 的 memo 和 emotional_design（融入写作指引段）
- [ ] 提示词已融入 writing-style 的 skill_layers（L1 结构层用于叙事约束、L2 内容层用于写作原则段、L3 审查层保留给 Phase 5 质量检查）
- [ ] 提示词中 writing-style 四个字段的内容已融入 prose——缺失任何一个 subagent 都会放飞
- [ ] 正文已通过 anti-ai.yaml 的质量检查（含 AI 疲劳词、句式违规、章尾情绪缺口、情绪兑现检测）
- [ ] 正文已通过结构性句式癖好检测（grep 扫描 anti-ai.yaml structural_tic_patterns，各模式不超过阈值）
- [ ] 正文已写入 archives/ 目录（Phase 5 落盘）后再进入归档流程
- [ ] 归档后的 markdown 命名正确 (vol-{N}-ch-{M}-{slugified-title}.md)
- [ ] 角色 state_history 在归档时更新
- [ ] 角色 emotional_arc 在归档时追记
- [ ] hooks.yaml 在归档时更新（mention/resolve/defer），钩子健康检查已完成
- [ ] 跨章情绪单调检测已在归档时执行
- [ ] current-focus.md 滑动窗口审视已完成（每章归档后必做，3 章倍数节点必须引导作者主动更新）

