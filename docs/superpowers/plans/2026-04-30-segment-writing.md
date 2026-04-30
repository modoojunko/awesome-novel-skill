# Segment-Based Chapter Writing — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace single-subagent full-chapter writing with a serial pipeline of 5-7 small subagents, each writing one narrative-function segment (400-600 words), reducing drift and improving quality.

**Architecture:** Phase 4 gains a Step 0 that auto-decomposes chapter outlines into segments; Step 2 generates one complete prompt file per segment. Phase 5 runs subagents serially, each receiving the previous segment's actual ending text. After concatenation, quality checks + novel-review run before the full chapter reaches the author.

**Tech Stack:** YAML templates, markdown prompt files, Agent tool subagent calls.

---

### Task 0: Add `segments` field to chapter.yaml.template

**Files:**
- Modify: `scripts/templates/chapter.yaml.template`

- [ ] **Step 1: Add segments field after emotional_design section**

Read `scripts/templates/chapter.yaml.template`. After the `micro_payoffs` block (the last item under `emotional_design`), insert:

```yaml
# ============================================================
# 叙事功能段落（Phase 4 Step 0 自动拆分，作者确认后写入）
# ============================================================
segments:
  - seg_number: 1
    function: ""           # atmosphere / character_beat / dialogue_push / action_beat / revelation / emotional_landing / transition
    goal: ""               # 这个段落要完成什么（一句话）
    what_to_write: ""      # 具体写什么（3-5句叙述，subagent据此写作）
    characters: []         # 出场角色
    emotional_tone: ""     # 情绪基调（紧张/放松/好奇/温情/压抑/爽快/悲伤）
    word_target: 500       # 字数目标
    ends_with: ""          # 段落结束时的画面/状态——下一段 subagent 的锚点
    dialogue_intent: ""    # 对话意图（仅 dialogue_push 填写：说服/试探/拒绝/转移/暗示/攻击/隐藏）
    micro_payoff: null     # 微兑现类型（仅承担微兑现的段落填写：info/relationship/emotion/clue/ability/resource/recognition）
```

- [ ] **Step 2: Verify template is valid YAML**

```bash
python -c "import yaml; yaml.safe_load(open('scripts/templates/chapter.yaml.template'))" && echo "valid"
```
Expected: `valid`

- [ ] **Step 3: Commit**

```bash
git add scripts/templates/chapter.yaml.template
git commit -m "feat: add segments field to chapter template for narrative-function decomposition"
```

---

### Task 1: Add Step 0 (segment decomposition) to novel-prompt

**Files:**
- Modify: `skills/prompt/SKILL.md`

- [ ] **Step 1: Add Step 0 section after "进入门禁" block and before "## 第一轮：视角转换"**

Find the line `## 第一轮：视角转换` in `skills/prompt/SKILL.md`. Insert before it:

```markdown
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
```

- [ ] **Step 2: Verify the edit is consistent with existing HARD-GATE and flow**

Read through `skills/prompt/SKILL.md` to confirm:
- HARD-GATE is still present before Step 0
- Step 0 sits between 进入门禁 and 第一轮：视角转换
- Step 0's STOP point is clear (author confirms segments before proceeding)
- Step 1 (视角转换) and Step 2 (三层合并) are NOT affected structurally

- [ ] **Step 3: Commit**

```bash
git add skills/prompt/SKILL.md
git commit -m "feat: add Step 0 segment decomposition to Phase 4 prompt skill"
```

---

### Task 2: Modify Step 2 (三层合并) to generate per-segment prompts

**Files:**
- Modify: `skills/prompt/SKILL.md`

- [ ] **Step 1: Replace "## 第二轮：三层合并" with segment-aware version**

The existing 第二轮 section generates one chapter prompt. Replace it to generate N segment prompts.

Old section starts at `## 第二轮：三层合并`. Replace the entire section (including sub-sections 1-6) with:

```markdown
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
  - 禁止使用 {fatigue_words_zh 中 abstract_emotion 和 cliche_action 类}
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
```

- [ ] **Step 2: Verify consistency**

Check that:
- The new Step 2 still references 视角转换 from Step 1 (视角转换 is NOT removed)
- The global-prompt.md and volume-prompt.md references are correct
- The `{%%PREV_SEGMENT_ENDING%%}` placeholder is clearly defined for Phase 5 to find and replace
- STOP points are clear

- [ ] **Step 3: Commit**

```bash
git add skills/prompt/SKILL.md
git commit -m "feat: replace single-chapter prompt generation with per-segment prompts in Phase 4"
```

---

### Task 3: Replace single-subagent write with serial segment pipeline

**Files:**
- Modify: `skills/write/SKILL.md`

- [ ] **Step 1: Rewrite Step 1 (调 Subagent 写正文)**

Replace the existing "## Step 1: 调 Subagent 写正文" section (the single Agent() call) with:

```markdown
## Step 1: 串行 Subagent 写各 Segment

读取 chapter.yaml 的 segments 列表，按序号串行执行。

```
for seg in 1..N:
    # 1. 读取本段提示词
    prompt_file = prompts/vol-{N}-ch-{M}-seg-{S}-prompt.md
    
    # 2. 若 seg ≥ 2，将 {%%PREV_SEGMENT_ENDING%%} 替换为上一段的实际结尾 200 字
    if seg >= 2:
        替换 prompt_file 中的 {%%PREV_SEGMENT_ENDING%%} 为：
        "上一段结尾原文（从这里接）：> {prev_segment_last_200_chars}"
    
    # 3. 调 subagent
    Agent(
      description: "写第{N}卷第{M}章 Segment {S}/{N}",
      subagent_type: "general-purpose",
      prompt: "读取 {prompt_file}。该文件是你的完整写作指令——包含全局写作方法论、故事背景、本段写作指引。

严格按文件中的所有要求写作。字数必须达到 word_target 指定的目标（不低于 80%，不超过 120%）。

关键约束：
- 你只写这一段，不写整章。段长 {word_target} 字左右。
- 如果写作指引中有'上一段结尾原文'，你的第一句话必须从那个画面无缝接续。
- 结尾必须停在 ends_with 指定的画面/状态。不要超出。
- 只输出小说正文。禁止出现解释、说明、注释、'以下是正文'等引导语。
"
    )
    
    # 4. 提取本段结尾 200 字，供下一段使用
    prev_segment_last_200_chars = 提取 subagent 输出的最后 200 字
```

**段落衔接规则：**
- Segment 1 无上一段——从零开始
- Segment 2..N：上一段结尾 200 字注入后，subagent 第一句话必须自然接续
- 主 Agent 不在段之间添加任何过渡文字——subagent 自己负责衔接
```

- [ ] **Step 2: Rewrite Step 2 (质量检查) to include concatenation**

Replace the existing "## Step 2: 质量检查" section with:

```markdown
## Step 2: 拼接 + 质量检查 + 深度评审

所有 segment 写完并通过字数检查后：

### 2a. 拼接正文

将 seg-1 到 seg-N 的输出按序拼接，段间不加任何分隔符或过渡语。保存为临时全文。

### 2b. 15 项质量检查

对拼接后的全文执行以下检查。检测依据：`settings/anti-ai.yaml` 的 8 个规则组。

| # | 检查项 | 不通过处理 |
|---|--------|-----------|
| 1 | 字数不达标 | 报告实际字数 vs 要求，列出各 segment 字数分布 |
| 2 | 上帝视角摘要 | 摘出典型句，特别检查 segment 衔接处是否出现了"接着""然后"等生硬过渡 |
| 3 | 违反核心约束 | 指出违规条款和位置 |
| 4 | 夹带非正文内容 | 指引导语、解释、文末总结 |
| 5 | AI疲劳词触发 | 扫描 fatigue_words，报告风险等级 |
| 6 | AI句式违规 | 连续同结构开头、列表式叙述、说明书式对话 |
| 7 | 结构性句式癖好 | grep 扫描 structural_tic_patterns |
| 8 | 章尾情绪缺口 | segment N（emotional_landing）是否留下了有效钩子？ |
| 9 | 情绪兑现检测 | pay_off旧缺口？make_new缺口？ |
| 10 | 跨章情绪单调 | 最近 3-5 章 primary_mood 连续相同？ |
| 11 | 微兑现缺失 | 本章至少一处"有收获"段落？过渡章达标？ |
| 12 | 安全着陆 | 结尾所有冲突完美解决？ |
| 13 | 物品/状态一致性 | 跨 segment 检查——物品消耗后仍使用？突然出现未交代物品？ |
| 14 | 句式单调检测 | 连续 4 句相同主语/连词开头？短/长句数量？ |
| 15 | 身体反应模板化 | "眼神/心里/喉咙/手心"密度 > 5次/500字？跨 segment 统计 |

任意一项触发 → **不展示正文**，报告问题，由作者决定：重写单个 segment / 重写全章 / 手动修改。

### 2c. 深度评审

全部质量检查通过后，触发 `novel-review` 进行 10 维 60+ 细项诊断。评审报告与正文一起展示给作者。

触发方式：
```
Skill(
  skill: "novel-review",
  args: "评审第{N}卷第{M}章"
)
```
```

- [ ] **Step 3: Rewrite Step 3 (作者审阅) to include review report**

Replace the existing "## Step 3: 作者审阅" with:

```markdown
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
```

- [ ] **Step 4: Update "下一步" section**

Replace the existing "## 下一步" with:

```markdown
## 下一步

作者满意后说"归档"→ Phase 6（`novel-archive`）。需修改时说"修改第X段"或"重写 seg-X"。需重新生成时说"重写全章"。
```

- [ ] **Step 5: Verify flow**

Read through the complete `skills/write/SKILL.md` and verify:
- Entry gate still checks `prompts/vol-{N}-ch-{M}-seg-{1}-prompt.md` existence (updated from single prompt file)
- Step 1 serial loop is clear and unambiguous
- Step 2 contains concatenation → 15 checks → novel-review in correct order
- Step 3 presents prose + review together
- All STOP points and HARD-GATEs are preserved

- [ ] **Step 6: Commit**

```bash
git add skills/write/SKILL.md
git commit -m "feat: replace single-subagent write with serial segment pipeline + pre-review quality gate"
```

---

### Task 4: Update entry gates for segment-based prompts

**Files:**
- Modify: `skills/prompt/SKILL.md` (进入门禁)
- Modify: `skills/write/SKILL.md` (进入门禁)
- Modify: `skills/archive/SKILL.md` (归档前完整性检查)

- [ ] **Step 1: Update prompt skill entry gate**

In `skills/prompt/SKILL.md`, update the 进入门禁 table:

Old:
```
| 章纲完整性 | memo（7段）+ emotional_design 全部有值？任一为空 → **STOP**，退回 `novel-outline` |
```

Add a new row after it:
```
| segments 已存在？ | 若 chapter.yaml 已有 segments（非空列表），跳到 Step 0 仅展示不重新拆分，等作者确认或调整 |
```

- [ ] **Step 2: Update write skill entry gate**

In `skills/write/SKILL.md`, update the 进入门禁 table:

Old:
```
| `prompts/vol-{N}-ch-{M}-prompt.md` 存在？ | 不存在 → **STOP**，退回 `novel-prompt` |
```

Replace with:
```
| `prompts/vol-{N}-ch-{M}-seg-{1}-prompt.md` 存在？ | 不存在 → **STOP**，退回 `novel-prompt` |
```

- [ ] **Step 3: Update archive skill entry gate**

In `skills/archive/SKILL.md`, update the 归档前完整性检查 table:

Old:
```
| `prompts/vol-{N}-ch-{M}-prompt.md` 存在？ | 不存在 → 退回 `novel-prompt` |
| 提示词覆盖所有 key_points？ | 对照 outline.key_points。缺失 → 退回 `novel-prompt` |
```

Replace with:
```
| 所有 segment 提示词文件存在？ | `prompts/vol-{N}-ch-{M}-seg-{1..N}-prompt.md` 全部存在？缺失 → 退回 `novel-prompt` |
| 提示词覆盖所有 key_points？ | 对照 outline.key_points + segments 列表。缺失 → 退回 `novel-prompt` |
```

- [ ] **Step 4: Commit**

```bash
git add skills/prompt/SKILL.md skills/write/SKILL.md skills/archive/SKILL.md
git commit -m "fix: update entry gates for segment-based prompt file naming"
```

---

### Task 5: Final integration verification

**Files:** All modified files

- [ ] **Step 1: Verify complete cross-file consistency**

Check the following chains hold:

1. **Template → Prompt**: chapter.yaml.template `segments` field is correctly referenced in prompt SKILL.md Step 0 and Step 2
2. **Prompt → Write**: prompt SKILL.md Step 2 generates `vol-{N}-ch-{M}-seg-{S}-prompt.md` files; write SKILL.md Step 1 reads `vol-{N}-ch-{M}-seg-{S}-prompt.md` files — naming matches
3. **Placeholder → Injection**: prompt SKILL.md writes `{%%PREV_SEGMENT_ENDING%%}`; write SKILL.md replaces it — string matches exactly
4. **Segment → Archive**: segments are NOT persisted past Phase 5 — archives receive full concatenated chapter (unchanged from current flow)
5. **Review timing**: novel-review runs AFTER quality checks, BEFORE author review — confirmed in write SKILL.md Step 2c and Step 3
6. **Backward compatibility**: Projects created before this change won't have `segments` in their chapter.yaml. The prompt skill should detect this (segments is empty/null) and proceed with Step 0 (fresh decomposition) — this is the default path, no special handling needed

- [ ] **Step 2: Run install script to verify no breakage**

```bash
./install.sh claude-code
```

Check that `~/.claude/skills/awesome-novel/` contains:
- Updated `skills/prompt/SKILL.md`
- Updated `skills/write/SKILL.md`
- Updated `scripts/templates/chapter.yaml.template`

- [ ] **Step 3: Commit final integration check**

```bash
git add -A
git commit -m "chore: integration verification — segment pipeline flow complete"
```
