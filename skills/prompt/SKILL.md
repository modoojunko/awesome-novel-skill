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

## 工具契约

| 工具 | 用途 | 限制 |
|------|------|------|
| Read | 读 chapter.md、writing-style.md、anti-ai.md、world-setting.md、角色文件、genre-example corpus | — |
| Write/Edit | 写 prompts/vol-{N}-ch-{M}-prompt.md | 不改 chapter.md status（由验收统一更新） |

## 执行前提

| 检查项 | 操作 |
|--------|------|
| 章纲完整性 | memo（8段）+ emotional_design 全部有值？任一为空 → **STOP**，返回主流程 |
| genre_profile 已选择？ | 读取 `settings/writing-style.md` 的 genre_profile 字段。为空 → **STOP**，列出 `$NOVEL_SKILL_HOME/references/genre-example/index.md` 下可用类型让作者选择 |
| 约束文件完整？ | writing-style.md + anti-ai.md 存在且有值？缺 → 返回主流程 |

## Step 1: 读取输入源

1. **writing-style.md** → 提取 core_principles、possible_mistakes、pov_consistency、depiction_techniques、genre
2. **chapter.md** → 提取 outline、memo、emotional_design、payoff_plan
3. **genre-example** → 读 index.md 找 genre_profile 对应的 corpus，取 `提示词注入段`（模块 5 用）；variant 文件存在则合并覆盖
4. **anti-ai库** → 读 `references/anti-ai/common-rules.md`（通用规则）+ `references/anti-ai/{genre}.md`（题材规则，如文件存在）

## Step 2: 按指南填充提示词

Read `references/prompt-setting-style.md`，按以下顺序执行：

1. **模块 1-3（基础定位/前置承接/人物状态）** — 按指南"核心填充方法"的输入源映射表，从 Step 1 的输入源直接提取填充
2. **模块 4（本章叙事任务）** — 按指南的场景分解方法切分场景：
   - 根据边界信号（换地点/跳时间/情绪转折）确定场景数（2-4 个）
   - 每个场景填种子三字段（前置状态/核心事件/收尾落点）
   - 填分段叙事入口（画面重入/情绪导向/节奏点）
   - 从章纲提取约束与边界、核心情绪落点、爽点与跌宕设计
3. **模块 5（文字与细节要求）** — 组装顺序：genre-example基础内容 → 通用反AI规范 → 题材反AI正反例：
   - 用 Step 1 读取的 genre-example `提示词注入段` 填入视角、描写要求、节奏、禁止项
   - 追加 `anti-ai/common-rules.md` 的通用反AI规范（疲劳词阈值 + 句式规则 + 元叙事禁止）
   - 追加 `anti-ai/{genre}.md` 的题材正反例（高频AI病句 ❌/✅ 对照，如文件存在）
4. **模块 6（真人感补充）** — 从章纲 memo + 作者补充提取无用细节和情绪波动，语言风格照搬 writing-style

全部填完后全局通读一次——掩住字段名，看每个种子读起来是叙事画面还是写作指令。

**[Checkpoint]** 展示完整提示词给作者确认，确认后保存。

## 保存

写入 `prompts/vol-{N}-ch-{M}-prompt.md`。**不更新 chapter.md status**——由主流程验收通过后统一更新。

## 验收

本 skill 不自己做验收。验收由 `skills/prompt-verify/SKILL.md` 独立执行——读 `references/prompt-setting-style.md` Section 三逐条检查 6 模块完整性、writing-style 注入、字数目标和视角锁定。

## 下一步

**状态汇报 + 自动路由：**
- ✅ 章纲：`chapters/vol-{N}-ch-{M}.md` → `status: outline`
- 📄 提示词：`prompts/vol-{N}-ch-{M}-prompt.md` → 已生成
- → 主流程检测到 `status=outline` + prompt 存在，**分发到提示词验收**（`skills/prompt-verify/SKILL.md`）

回到主流程，由主 SKILL.md 检测进度并分发到验收。
