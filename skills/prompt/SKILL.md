---
name: novel-prompt
description: 章提示词生成与视角转换。Phase 4。当章纲已确认、需要为 subagent 准备完整写作指令时必须使用——视角转换 + 三层提示词合并（全局+卷+章专属）。触发："生成提示词""视角转换""组装章提示词""准备写作材料"。写正文前必须经此步骤，不可跳过直接写。
---

# Novel Prompt — 章提示词生成

## Overview

视角转换 + 三层合并：全局提示词全文 + 卷提示词全文 + 本章专属 prose → 一个格式文件。subagent 只读这一个文件。

**When NOT to use:** 章纲不完整（memo 或 emotional_design 缺失）、本章提示词已生成且未修改章纲、章状态尚未到 outline。

**Announce at start:** "我来生成本章提示词。先做视角转换。"

## HARD-GATE

```
视角转换必须先单独确认，确认后才能组装章提示词。严禁合并确认。
章提示词 = 全局全文 + 卷全文 + 本章专属。subagent 只读这一个文件。
```

## 进入门禁

| 检查项 | 操作 |
|--------|------|
| `prompts/global-prompt.md` 是否存在？ | 不存在 → 生成（从 writing-style.yaml），作者确认 |
| `prompts/volume-{N}-prompt.md` 是否存在？ | 不存在 → 生成（从 volume.yaml + archives/），作者确认 |
| 模板版本检查 | 读取 `~/.claude/skills/novel/scripts/templates/writing-style.yaml.template` 头部 `# version: N`，对比项目 `settings/writing-style.yaml` 头部版本号。模板版本更高 → 向作者报告"写作风格模板有更新"，列出新增的 global_rules 和 possible_mistakes 条目，问作者"合并新规则 / 暂不合并"。合并后自动重新生成 `prompts/global-prompt.md` |
| 章纲完整性 | memo（7段）+ emotional_design 全部有值？任一为空 → **STOP**，退回 `novel-outline` |
| segments 已存在？ | 若 chapter.yaml 已有 segments（非空列表），跳到 Step 0 仅展示不重新拆分，等作者确认或调整 |
| author-intent.md 一致性 | 本章与核心主题一致 / 存在偏离？偏离 → **STOP** |
| current-focus.md 一致性 | 本章在优先级范围内 / 偏离？偏离 → **STOP** |

## Step 0: 叙事功能段落拆分

门禁通过后，Agent 自动将章纲拆分为 5-7 个叙事功能段落（segment），展示给作者确认后写入 chapter.yaml。

### 段落功能类型

| 类型 | 作用 | 分配原则 |
|------|------|---------|
| `atmosphere` | 氛围建立——环境描写、五感锚定、世界基调 | 首段常用，让读者先站稳 |
| `character_beat` | 角色状态——习惯/情绪/内心活动，建立读者连接 | 首段或事件后使用 |
| `dialogue_push` | 对话推进——有意图的对话，推动信息或关系变化 | 每个 key_point 如涉及重要对话 |
| `action_beat` | 动作事件——冲突、动作、关键事件发生 | 每个 key_point 如涉及动作/事件 |
| `revelation` | 信息揭露——新线索、真相浮现、伏笔推进 | 每个 key_point 如涉及信息释放 |
| `emotional_landing` | 情绪落地——事件余波、角色反应、章末钩子 | **末段必须** |
| `transition` | 过渡桥接——时间/地点/情绪转换 | 仅必要时使用 |

### 拆分流程

1. 读取 chapter.yaml 的 outline + memo + emotional_design
2. 按以下规则拆分为 5-7 个 segment：
   - **首段**：必须是 `atmosphere` 或 `character_beat`——先让读者站稳，不急着推剧情
   - **中间段**：每个 key_point 映射为 1-2 个 segment，选择匹配的 function 类型
   - **末段**：必须是 `emotional_landing`——事件后的情绪余波 + 章末钩子（对应 emotional_design.emotional_hook）
   - **transition**：只在时间跳转/地点切换/情绪大转折时插入，不滥用
   - 总 word_target 之和 ≈ 章纲字数下限
   - emotional_tone 序列必须匹配 mood_progression（从X→经Y→以Z结束）
3. 为每个 segment 填写：
   - `function`：从 7 种类型中选择
   - `goal`：一句话描述本段目标
   - `what_to_write`：3-5 句叙述，描述本段具体写什么。**不写对话、不写动作细节**，只描述事件和走向
   - `characters`：本段出场角色
   - `emotional_tone`：本段情绪基调
   - `word_target`：字数目标（500-600 字）
   - `ends_with`：本段结尾的画面/状态——**这是下一个 subagent 的锚点**。必须是一个可感知的具体画面或状态，不是概述
   - `dialogue_intent`：仅 `dialogue_push` 填写（说服/试探/拒绝/转移/暗示/攻击/隐藏）
   - `micro_payoff`：如果本段承担某个微兑现，填写对应的微兑现 type
4. 检查：
   - key_points 是否全部有对应的 segment？
   - emotional_tone 序列是否与 mood_progression 一致？
   - 章末 emotional_landing 是否留下了 emotional_hook 类型的钩子？
   - 总字数是否接近章纲字数下限？
5. **STOP：展示全部 segment 列表给作者确认/调整。确认后写入 chapter.yaml 的 segments 字段。**

### 拆分示例

章纲 key_points：
  - "委托人讲述女儿失踪经过"
  - "走访出租屋，找到未带走的充电器"
  - "物流公司同事说法有矛盾"
  - "朋友圈地址查无此址"
mood_progression：日常松弛→好奇→紧张→悬念收束

拆分为 6 个 segment：

| # | function | goal | word_target |
|---|----------|------|-------------|
| 1 | atmosphere | 老城区早晨的市井气息，陆征的日常 | 400 |
| 2 | dialogue_push | 委托人讲述失踪经过，陆征接案 | 600 |
| 3 | character_beat | 陆征独自整理信息，决定先走访出租屋 | 400 |
| 4 | action_beat | 走访出租屋，发现未带走的充电器 | 500 |
| 5 | revelation | 物流公司同事说法矛盾，朋友圈地址查无此址 | 600 |
| 6 | emotional_landing | 陆征看着地图上的空地址，买了一包烟 | 500 |

## 第一轮：视角转换

1. 读取 chapter.yaml 的 outline 字段
2. **确认叙事视角**：读 narrative_pov。空 → 询问作者确认（第三人称有限/第一人称/全知）
3. 按视角转换规则将上帝视角章纲转为沉浸式写作指引
4. **STOP：展示（含叙事视角），等确认。**

### 视角转换规则

一句话：**把"发生了什么事"重写为"事情发生时，在场的人感受到了什么"。**

- 禁止"本章讲述了""主角经历了"等上帝视角概述语
- 指引是地图，不是已经走完的路。只描述场景基调、关键情节点、情感走向，把叙事节奏和语言组织留给 subagent
- **字数上限**：不超过章纲 outline 字数的 2-3 倍
- **禁止写具体对话**：只描述对话的目的和走向
- **禁止写动作细节**：只描述动作的结果和意义
- 写完自检——如果 subagent 照着做文字整理就能交稿 → 粒度太细了

### 钩子兑现锚定

若 payoff_plan 有 resolve 或 partial_advance 的钩子 → 必须将 seed_text 嵌入写作指引："> 读者在第 X 章看到过：'[原文引用]'——本章需要接着这个画面来写兑现。"

### 爽感循环感知

读取 cycle_position，注入对应策略：
- **压制章**：写具体的"债"，不写"主角很惨"；压制比上一轮更过分；章尾暗示"快了"
- **释放章**：对应压制章的每一笔债怎么打回去；反派表情 不在乎→慌→崩溃；旁观者反应；余波
- **余波章**：释放后世界变了什么；埋新压制种子

## 第二轮：生成 Per-Segment 提示词

视角转换确认后，为每个 segment 生成一个**独立完整的提示词文件**。每个文件包含完整的全局上下文 + segment 专属写作指引。subagent 只读一个文件就能写。

**输出文件**：`prompts/vol-{N}-ch-{M}-seg-{S}-prompt.md`（S 从 1 到 N）

### 提示词结构（每个 segment 文件相同结构）

```
## 角色定位
[来自 prompts/global-prompt.md，原样，所有 segment 完全相同]

## 写作原则与禁忌
[来自 prompts/global-prompt.md，原样，所有 segment 完全相同]

## 故事背景
[组装方式同旧版：world-setting 全局规则 + 场景片段 + 角色快照 + 前章锚定 + 活跃钩子速览]
[所有 segment 完全相同，因为同一章的世界背景不变]

## 写作指引
[本 segment 专属]
- 叙事功能：{function} — {goal}
- 你要写的是：{what_to_write}
- 情绪基调：{emotional_tone}
- 出场角色：{characters}
- 角色在本段的动机/状态：[从角色 yaml 提取与当前段落相关的状态]
- 本段结束画面：{ends_with}

[以下仅 seg ≥ 2 时注入——Phase 5 写入上一段实际结尾原文后替换此占位符]
{%%PREV_SEGMENT_ENDING%%}

[以下仅 dialogue_push 段注入]
- 对话意图：{dialogue_intent}。对话是微型动作——角色的每句话都是试探、拒绝、转移、暗示或攻击。禁止说明书式对话（角色互相告知已知信息）。

[以下仅承担微兑现的段注入]
- 微兑现要求：本段需给出 {micro_payoff} 类型的微兑现——{从 emotional_design.micro_payoffs 中取对应 description}

## 写作要求
- 字数目标：{word_target} 字。不少于目标的 80%，不超过目标的 120%
- 叙事视角：{narrative_pov}
- 句式规则：主体叙事用中长句，短句用于节奏切断。相邻 4 句不得以相同代词或连词开头。单段不超过 5 行。
- 禁止事项：
  - 禁止上帝视角概述（"本章讲述了""他意识到"）
  - 禁止直接描述感受（"他很愤怒"→写动作和身体反应）
  - 禁止文末总结升华
  - 禁止提前写 ends_with 之后的内容——停在 ends_with 的画面
  - 禁止使用 fatigue_words_zh 中 abstract_emotion 和 cliche_action 类词汇
  [若 memo.prohibitions 非空，追加：本章禁止：{prohibitions}]
```

### 生成步骤

1. 读取 `prompts/global-prompt.md` → 提取"角色定位"和"写作原则与禁忌"两段原文
2. 按旧版方法组装"故事背景"段（world-setting + 角色快照 + 前章锚定 + 活跃钩子）
3. 对每个 segment：
   a. 组装"写作指引"段（function/goal/what_to_write/emotional_tone/characters/ends_with/dialogue_intent/micro_payoff）
   b. 组装"写作要求"段（word_target + 视角 + 句式规则 + 禁止事项）
   c. 对 seg ≥ 2 的 segment，在"写作指引"末尾插入占位符 `{%%PREV_SEGMENT_ENDING%%}`——Phase 5 串行写作时由主 Agent 替换为上一段实际结尾 200 字
4. 保存 `prompts/vol-{N}-ch-{M}-seg-{S}-prompt.md`

### 视角转换适配

视角转换（第一轮）的结果应用到每个 segment 的 what_to_write 中——确保每个 segment 的 what_to_write 已经经过了视角转换（上帝视角→沉浸式指引）。

### 变体策略

不再生成 3 个变体。作者在 Step 0 确认 segment 拆分时已确定了叙事走向——segment 的 function 序列和 ends_with 链已锁定了节奏。每个 segment 只生成一个提示词。

### STOP：展示一个代表性 segment 的完整提示词作为样例，确认后批量生成全部文件。

确认后，将 chapter.yaml status 更新为 `draft`，prompt_path 替换为 segment 文件列表。

## 下一步

完成后引导进入 Phase 5。当作者说"写正文"时，母技能路由到 `novel-write`。
