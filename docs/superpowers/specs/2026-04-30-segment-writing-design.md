# Segment-Based Chapter Writing — Design Spec

Date: 2026-04-30
Status: approved

## Problem

当前 subagent 一次性写整章 3000-4000 字，任务粒度过大，经常跑偏、偏离章纲、结尾疲软。需要将章节拆分为更小的叙事功能段落（5-7 个 segment，每个 400-600 字），由独立 subagent 串行写作，每个 subagent 只承担一个小任务。

## Concept

**拆分的不是场景（地点切换），是叙事功能段落（意图切换）。**

一章通常 1-2 个场景，但叙事功能可以拆成 5-7 段：氛围建立 → 角色状态 → 对话推进 → 动作事件 → 信息揭露 → 情绪余波 → 章末钩子。

## Segment Function Types

| 类型 | 作用 | 典型内容 |
|------|------|---------|
| `atmosphere` | 氛围建立 | 环境描写、五感锚定、世界基调 |
| `character_beat` | 角色状态 | 角色的习惯/情绪/思考，建立读者连接 |
| `dialogue_push` | 对话推进 | 有意图的对话，推动信息或关系变化 |
| `action_beat` | 动作事件 | 冲突、动作、关键事件发生 |
| `revelation` | 信息揭露 | 新线索、真相浮现、伏笔回收 |
| `emotional_landing` | 情绪落地 | 事件后的余波、角色反应、章末钩子 |
| `transition` | 过渡桥接 | 时间/地点/情绪之间的过渡 |

## Segment Spec (per chapter.yaml)

```yaml
segments:
  - seg_number: 1
    function: "atmosphere"
    goal: ""
    what_to_write: ""
    characters: []
    emotional_tone: ""
    word_target: 500
    ends_with: ""
    dialogue_intent: ""     # 仅 dialogue_push 填写
    micro_payoff: null      # 仅承担微兑现时填写
```

## Overall Flow

```
Phase 3 → 章纲（不变）
Phase 4 → Step 0: 自动拆 segment → 作者确认
          Step 1: 视角转换（不变）
          Step 2: 生成 per-segment 完整提示词
Phase 5 → 串行 subagent 写各 segment → 拼接 → 15项检查 → novel-review → 作者审阅
Phase 6 → 归档（不变）
```

## Phase 4 Changes

### Step 0: Segment Decomposition (NEW)

Input: chapter.yaml (outline + memo + emotional_design)
Output: 5-7 segment specs, displayed to author for confirmation

Rules:
1. First segment MUST be `atmosphere` or `character_beat` — ground the reader first
2. key_points map to `action_beat` / `dialogue_push` / `revelation` segments
3. Last segment MUST be `emotional_landing` — aftermath + chapter-end hook
4. `transition` only when time/location/emotional jumps exist
5. emotional_tone sequence MUST match mood_progression
6. Total word_target ≈ chapter word target

### Step 2: Per-Segment Prompt Generation

Each segment gets its own complete prompt file at `prompts/vol-{N}-ch-{M}-seg-{S}-prompt.md`.

Structure:
```
## 角色定位
[global-prompt.md, unchanged]

## 写作原则与禁忌
[global-prompt.md, unchanged]

## 故事背景
[world-setting + volume context + character snapshots, unchanged per chapter]

## 写作指引
[segment-specific: what_to_write + function + emotional_tone + ends_with]
[if seg >= 2: "上一段结尾原文：> [actual 200 chars from previous segment output]"]
[character motivation/state for this segment]

## 写作要求
[word_target + sentence rules + segment-specific prohibitions]
```

Global + volume sections are IDENTICAL across all segments of the same chapter.

## Phase 5 Changes

### Writing Pipeline (Serial)

```
for seg in 1..N:
    subagent reads prompts/vol-{N}-ch-{M}-seg-{S}-prompt.md
    subagent writes segment prose
    main agent extracts last 200 chars
    main agent injects into seg+1 prompt file (# only if seg+1 exists)
```

### Post-Writing (after all segments complete)

1. Main agent concatenates all segment prose into full chapter
2. Run 15-item quality check on full chapter
3. Run novel-review (10-dimension deep review)
4. Present prose + review report to author together
5. Author: accept / modify / regenerate individual segments

### Regeneration

Author can request regeneration of a single segment without rewriting the whole chapter:
- "重写 seg-3" → only that segment, using seg-2's actual ending as anchor
- "重写全章" → all segments in sequence

## Files Affected

| File | Change |
|------|--------|
| `scripts/templates/chapter.yaml.template` | Add `segments: []` field |
| `skills/prompt/SKILL.md` | Add Step 0 (segment decomposition), modify Step 2 (per-segment prompts) |
| `skills/write/SKILL.md` | Replace single subagent call with serial pipeline + concatenation + review before author review |

## Unchanged

- Phase 1, 2, 3 — no changes
- Phase 6 — no changes (archives receive full chapter, not segments)
- `novel-review` — no changes (reviews full chapter, not segments)
- All templates except chapter.yaml.template — no changes
- `global-prompt.md` and `volume-{N}-prompt.md` — unchanged, still injected per-segment
