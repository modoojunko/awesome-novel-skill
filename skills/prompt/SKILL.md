---
name: novel-prompt
description: 章提示词生成——从章纲生产 prompt.md。触发：章纲确认后自动分发或手动"生成本章提示词"。完成后回到主流程。
---

# Novel Prompt — 章提示词生成

> 读输入源 → 读 `references/prompt-setting-style.md` → 按指南 9 层骨架填充。每步确认。验收由主流程独立执行。

## Overview

将章纲 + writing-style + genre-profile 生产为 subagent 可执行的 prompt.md。按指南的 9 层骨架填充，指南定义了每个字段的输入源和填充原则。填充完成后保存，验收由主流程执行。

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

1. **writing-style.md** → 提取四字段（core_principles、possible_mistakes、depiction_techniques）+ genre + model
2. **volume.md** → 提取**前一章**的章名、结尾画面、情绪落点（在卷纲的 chapters_summary 中）
3. **chapter.md** → 提取 memo、emotional_design、outline（场景分解）、payoff_plan
4. **角色设定文件** → 读取涉及的角色，提取本章相关状态
5. **genre-example** → 读 index.md 找 genre_profile 对应的 corpus，取 `提示词注入段`（L8 用）
6. **anti-ai库** → 读 `references/anti-ai/common-rules.md` + `references/anti-ai/{genre}.md`（如存在）

**注意：L2 来龙只读卷纲中的前章摘要，不读上一章全文。**

## Step 2: 按指南填充 9 层

Read `references/prompt-setting-style.md`，按以下顺序填充：

1. **L1 元信息** — 从 writing-style.md + chapter.md 提取：题材/风格/字数/本章角色/模型
2. **L2 来龙** — 从 volume.md 前章摘要提取：结尾画面/情绪残留/缺口。**只读摘要，不读全文**
3. **L3 去脉** — 从 chapter.md memo 提取：核心悬念/悬念状态/读者感受
4. **L4 角色弧光** — 从 chapter.md 人物状态 + 角色文件提取：每角色起点→转折→落点 + 微习惯
5. **L5 场景序列** — 从 chapter.md outline 提取：
   - 按边界信号（换地点/跳时间/情绪转折）切分场景（2-4 个）
   - 每场景填种子三字段（入口画面/核心事件/出口画面）+ 情绪拐点
6. **L6 约束** — 从 chapter.md memo 提取：情节红线（2-4 条）+ 边界禁止 + 角色禁区
7. **L7 爽点设计** — 从 chapter.md memo 提取：类型/铺垫位置/释放位置/释放方式 + 克制点
8. **L8 文字规则** — 组装以下内容写入 L8 各字段：
   - 视角：从 genre-example `prompt_segment` 提取视角字段（如"第三人称限制"）
   - 描写要求：从 genre-example `prompt_segment` 提取描写手法/节奏/禁止项
   - 疲劳词阈值：从 anti-ai/common-rules.md 表一复制（如"突然≤3/章"）
   - 句式规则：从 anti-ai/common-rules.md 表二复制（如"连续4句主语不得相同"）
   - 元叙事禁止：从 anti-ai/common-rules.md 表三复制（如"禁止'读者'"）
   - 题材正反例：从 anti-ai/{genre}.md 复制（如存在）
   - **必须填入具体内容，不只是标注来源**
9. **L9 质感** — 从 chapter.md memo + 作者补充提取：无用细节/对话节奏/真人痕迹

**冲突检测：** 填完后检查 L2 情绪残留 = L4 第一角色起点、L7 释放位置在 L5 场景中存在。

全部填完后全局通读一次——掩住字段名，看每个种子读起来是叙事画面还是写作指令。

**[Checkpoint]** 展示完整提示词给作者确认，确认后保存。

## 保存

写入 `prompts/vol-{N}-ch-{M}-prompt.md`。**不更新 chapter.md status**——由主流程验收通过后统一更新。

## 验收

本 skill 不自己做验收。验收由 `skills/prompt-verify/SKILL.md` 独立执行——读 `references/prompt-setting-style.md` 第三部分逐条检查 9 层完整性、冲突检测、writing-style 注入。

## 下一步

**状态汇报 + 自动路由：**
- ✅ 章纲：`chapters/vol-{N}-ch-{M}.md` → `status: outline`
- 📄 提示词：`prompts/vol-{N}-ch-{M}-prompt.md` → 已生成
- → 主流程检测到 `status=outline` + prompt 存在，**分发到提示词验收**（`skills/prompt-verify/SKILL.md`）

回到主流程，由主 SKILL.md 检测进度并分发到验收。
