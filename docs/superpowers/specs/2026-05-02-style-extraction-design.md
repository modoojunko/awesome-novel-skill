# Style Extraction Sub-Agent Design

Date: 2026-05-02
Status: approved

## Input

The author provides a plain-text file (`.txt`, UTF-8) of the reference novel. The file is placed in the project root or a path the author specifies.

## Skill File

New file: `skills/style-extract/SKILL.md` — follows the same sub-skill convention as `skills/write/SKILL.md`, `skills/prompt/SKILL.md`, etc. Registered in the main SKILL.md Phase 2 routing table.

## Purpose

Add a `novel-style-extract` sub-skill that learns writing style from a reference novel (single book), extracts quantifiable and qualitative style rules, and injects them into the existing awesome-novel workflow (writing-style.yaml + anti-ai.yaml + prompt few-shot examples).

## Architecture

New sub-skill `novel-style-extract`, triggered during Phase 2 (setting discussion) as an enhanced path for writing style configuration. Produces a **style profile** directory under the project, then merges into the active writing configuration upon author confirmation.

```
reference.txt
      │
      ▼
┌─────────────────────────────────────┐
│        novel-style-extract          │
│                                     │
│  Step 1: Statistical script        │
│  ├─ Sentence/paragraph/dialogue    │
│  └─ Output: style-metrics.yaml     │
│                                     │
│  Step 2: Qualitative Agent         │
│  ├─ Narrative distance, dialogue   │
│  │   tone, description patterns    │
│  ├─ Select 8-12 few-shot excerpts  │
│  └─ Output: style-qualitative.yaml │
│           + examples.md            │
│                                     │
│  Step 3: Main Agent merge          │
│  └─ Output: style-profiles/{name}/ │
└──────────────┬──────────────────────┘
               │
               ▼
┌──────────────────────────────────────┐
│  Merge into project:                │
│  - writing-style.yaml fields        │
│  - anti-ai.yaml thresholds/words    │
│  - global-prompt.md examples block  │
│  - Per-segment prompt examples      │
└──────────────────────────────────────┘
```

Key design decision: style profiles are standalone files (`style-profiles/{name}/`). The author chooses when to apply them — one extraction, reusable across projects.

## Step 1: Statistical Analysis Script

File: `scripts/analyze_style.py`

Input: reference novel as plain text (UTF-8)
Output: `style-metrics.yaml`

### Metrics extracted

| Field | Method | Maps to |
|-------|--------|---------|
| `sentence_length` | Sentence length distribution (by 。！？；): short(<10), medium(10-40), long(>50) ratios, mean, variance | `core_principles.natural_expression` sentence rules |
| `paragraph_length` | Paragraph length distribution (by blank line): mean, median, min, max, single-sentence paragraph ratio | `anti-ai.paragraph_rules` |
| `sentence_openings` | Top-20 sentence-initial word frequencies | `anti-ai.sentence_rules` opening diversity |
| `dialogue_ratio` | Quoted content word count / total word count; dialogue tag position distribution | `writing-style` dialogue rules |
| `punctuation_profile` | Comma/period/exclamation/ellipsis density per 1000 chars | `anti-ai.punctuation_rules` |
| `word_frequency` | Top-200 frequent words (excluding function words), adverb/conjunction focus | `anti-ai.fatigue_words` supplement + `possible_mistakes` supplement |
| `idiom_density` | Four-character idioms per 500 chars (jieba segmentation + quad-char match) | `anti-ai.sentence_rules.max_idioms_per_500` |
| `adjective_adverb_density` | Adjectives/adverbs per 300 chars (POS tagging) | `anti-ai.sentence_rules.max_intensity_adverbs_per_300` |
| `description_ratio` | Environment description ratio (spatial/scenery keywords); psychological description ratio (想/觉得/感到/心里 keywords) | `core_principles` environment description constraint |
| `body_emotion_density` | Body part (眼/手/心/喉/眉/指) + emotion word density per 500 chars | `anti-ai.sentence_rules.max_body_emotion_per_500` |
| `structural_tic_usage` | Full-text count for each anti-ai.yaml structural_tic_pattern — calibrates thresholds | anti-ai threshold calibration |

### Implementation notes

- Dependencies: `jieba` (segmentation + POS tagging), pure Python regex for sentence splitting
- Text preprocessing: strip chapter title lines, normalize blank lines
- Output thresholds include confidence intervals (e.g., "short sentence ratio 32% ±5%")
- For texts >500k chars: sample first/middle/last 50k chars each, average results

## Step 2: Qualitative Analysis Agent

Input: reference text via layered sampling (~30-50k chars total)
Output: `style-qualitative.yaml` + `examples.md`

### Layered sampling strategy

| Layer | Source | Purpose |
|-------|--------|---------|
| Opening | First ~8000 chars | Author's first-impression strategy |
| Mid-body | 3 random 5000-char slices | Daily writing habits — dialogue rhythm, description density, transitions |
| Climax | 1-2 high-conflict sections (highest dialogue + emotion keyword density) | High-pressure scene handling |

### Analysis dimensions

| Dimension | Key questions | Output target |
|-----------|--------------|---------------|
| Narrative distance | How close is the reader to characters? Direct psych narration vs action-inferred? Does narrator editorialize? | `pov_consistency` rules |
| Dialogue tone | Written vs spoken register? Interruption/ellipsis/silence frequency? Tag preferences? Character voice differentiation? | `natural_expression` dialogue rules + `dialogue_rules` |
| Description patterns | Environmental description: functional or atmospheric? Sensory preferences? Metaphor type and density? | `description_vs_depiction` rules + `depiction_techniques` |
| Character voice | Can characters be distinguished by dialogue alone? Body reactions per-character? Secondary characters: tools or agents? | `character_building` rules |
| Emotion externalization | Which body parts convey which emotions? Restrained vs cathartic? Transition pacing (sudden vs layered)? | `depiction_techniques` supplement + `emotional_pacing` rules |
| Taboos & avoidances | What does this author NOT write? No direct emotion statements? No long environment? No idioms? No sexual/violent content? | `possible_mistakes` supplement + `genre.anti_cliches` |

### Agent prompt constraint

The agent must cite original text as evidence for every conclusion (excerpts ≤30 chars). Forbidden: empty praise ("文笔好", "节奏感强"). Required: actionable conclusions ("对话标签80%用'说/道'不加副词修饰").

### Few-shot excerpt selection (8-12 total)

| Type | Count | Purpose |
|------|-------|---------|
| Opening | 1-2 | Atmosphere establishment method |
| Action | 2-3 | Action description rhythm and granularity |
| Dialogue | 2-3 | Dialogue tone and rhythm |
| Emotion | 2 | Emotion externalization method |
| Transition | 1-2 | Scene switch / time passage handling |

Each excerpt annotated with: scene type, demonstrated style feature (one line), word count.

## Step 3: Main Agent Merge

### 3a. Merge into writing-style.yaml

Principle: **append only, never overwrite author-confirmed settings.**

| Source | Target field | Strategy |
|--------|-------------|----------|
| `style-metrics.sentence_length` | `natural_expression` | Convert ratios to natural-language rules |
| `style-metrics.paragraph_length` | `natural_expression` | Convert mean to paragraph constraint |
| `style-metrics.dialogue_ratio` | `natural_expression` | Dialogue density guideline |
| `style-qualitative.narrative_distance` | `pov_consistency` | Direct injection |
| `style-qualitative.dialogue_tone` | `natural_expression` dialogue rules | Direct injection |
| `style-qualitative.description` | `description_vs_depiction` | Append technique preferences |
| `style-qualitative.character_voice` | `character_building` | Append character rules |
| `style-qualitative.emotion` | `depiction_techniques` | Append or replace techniques |
| `style-qualitative.taboos` | `possible_mistakes` | **Append** to existing list |

Conflict resolution: when stats contradict qualitative agent (e.g., "dialogue is sparse" but stats show 38%), **defer to stats**. Numbers don't lie.

### 3b. Calibrate anti-ai.yaml

- **Adjust thresholds**: If reference text uses a tic pattern N times/chapter, set threshold to N+2
- **Add fatigue words**: Words with frequency <2 per 100k chars in reference → add to blocklist
- **Calibrate punctuation rules**: Based on reference punctuation profile
- **Calibrate paragraph rules**: Based on reference single-sentence paragraph ratio

### 3c. Inject few-shot examples

1. Add an "风格参考范例" block to `prompts/global-prompt.md` with all 8-12 excerpts
2. In Phase 4 per-segment prompts, append one type-matched excerpt:

| Segment function | Injected example type |
|-----------------|----------------------|
| `atmosphere` | Opening |
| `dialogue_push` | Dialogue |
| `action_beat` | Action |
| `emotional_landing` | Emotion |
| `transition` | Transition |

### 3d. Author confirmation gate

After merge, display change summary and STOP for author approval before writing files.

## Integration Points

| Phase | Integration |
|-------|-------------|
| Phase 2 | `novel-style-extract` offered as enhanced path during writing style discussion |
| Phase 4 | Few-shot examples injected into global-prompt.md and per-segment prompts |
| Phase 5 | Calibrated anti-ai thresholds used in 15-item quality check |
| All | Extracted rules persist in writing-style.yaml for all subsequent chapters |

## Output File Structure

```
style-profiles/{name}/
├── style-metrics.yaml       # Step 1 script output
├── style-qualitative.yaml   # Step 2 agent output
└── examples.md              # Step 2 agent output (few-shot excerpt pool)
```
