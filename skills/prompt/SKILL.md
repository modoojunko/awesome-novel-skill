---
name: novel-prompt
description: 章提示词生成——从章纲生产 prompt.md。触发：章纲确认后自动分发或手动"生成本章提示词"。完成后回到主流程。
---

# Novel Prompt — 章提示词生成

> 读输入源 → 读 `references/prompt-setting-style.md` → 按指南 6 模块骨架填充。每步确认。验收由主流程独立执行。

## Overview

将章纲 + writing-style + genre-profile 生产为 subagent 可执行的 prompt.md。按指南的 6 模块骨架填充，指南定义了每个字段的输入源和填充原则。填充完成后保存，验收由主流程执行。

**When NOT to use:** 章纲不完整（memo 或 emotional_design 缺失）、本章提示词已存在且未修改章纲、章状态尚未到 outline。

**Announce at start:** "我来生成本章提示词。先读输入源..."

## 执行前提

| 检查项 | 操作 |
|--------|------|
| 章纲完整性 | memo（8段）+ emotional_design 全部有值？任一为空 → **STOP**，返回主流程 |
| genre_profile 已选择？ | 读取 `settings/writing-style.md` 的 genre_profile 字段。为空 → **STOP**，列出 `$NOVEL_SKILL_HOME/references/genre-example/index.md` 下可用类型让作者选择 |
| 约束文件完整？ | writing-style.md + anti-ai.md 存在且有值？缺 → 返回主流程 |

## Step 1: 读取输入源

1. **writing-style.md** → 提取 core_principles、possible_mistakes、pov_consistency、depiction_techniques、genre
2. **anti-ai.md** → 提取 structural_tic_patterns（severity=high）、dialogue_rules、sentence_rules
3. **chapter.md** → 提取 outline、memo、emotional_design、payoff_plan
4. **genre-example** → 读 index.md 找 genre_profile 对应的 corpus，取 `提示词注入段`（模块 5 用）；variant 文件存在则合并覆盖

## Step 2: 按指南填充提示词

Read `references/prompt-setting-style.md`，按以下顺序执行：

1. **模块 1-3（基础定位/前置承接/人物状态）** — 按指南"核心填充方法"的输入源映射表，从 Step 1 的输入源直接提取填充
2. **模块 4（本章叙事任务）** — 按指南的场景分解方法切分场景：
   - 根据边界信号（换地点/跳时间/情绪转折）确定场景数（2-4 个）
   - 每个场景填种子三字段（前置状态/核心事件/收尾落点）
   - 填分段叙事入口（画面重入/情绪导向/节奏点）
   - 从章纲提取约束与边界、核心情绪落点、爽点与跌宕设计
3. **模块 5（文字与细节要求）** — 用 Step 1 读取的 genre-example `提示词注入段` 替换。无题材特定约束则用指南模板通用版
4. **模块 6（真人感补充）** — 从章纲 memo + 作者补充提取无用细节和情绪波动，语言风格照搬 writing-style

全部填完后全局通读一次——掩住字段名，看每个种子读起来是叙事画面还是写作指令。

**STOP：展示完整提示词给作者确认，确认后保存。**

## 保存

写入 `prompts/vol-{N}-ch-{M}-prompt.md`。**不更新 chapter.md status**——由主流程验收通过后统一更新。

## 下一步

回到主流程，由主 SKILL.md 检测进度并分发到下一步。
