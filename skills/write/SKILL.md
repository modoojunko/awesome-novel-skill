---
name: novel-write
description: 正文生成——根据提示词写完整章正文。触发：提示词验收通过后自动分发，或手动"写正文""写这章"。完成后回到主流程。
---

# Novel Write — 正文生成

> 读 prompt + chapter.md → 调 exec-prose agent 写作 → 验证输出。写作由子 agent 自主执行，主 Agent 做分发和验证。

## Overview

提示词验收通过后，主 Agent 调 `agents/pipeline/exec-prose.md` 子 agent 一次写完整章正文。主 Agent 不介入写作过程，只负责前置检查和输出验证。

**When NOT to use:** prompt 文件不存在、chapter.md status 非 draft、本章正文已存在且未要求重写。

**Announce at start:** "我来调写作 agent 生成本章正文。"

## 执行前提

| 检查项 | 操作 |
|--------|------|
| prompt 文件存在？ | `prompts/vol-{N}-ch-{M}-prompt.md` 不存在 → **STOP**，返回主流程走提示词生成 |
| chapter.md status = draft？ | 非 draft → **STOP**，提示词尚未验收通过 |
| 正文已存在？ | `archives/vol-{N}-ch-{M}-*.draft.md` 已存在 → 问作者"已存在草稿，覆盖还是继续编辑？" |

## Step 1: 准备

1. 确认卷号 `{N}` 和章号 `{M}`
2. 读取 `prompts/vol-{N}-ch-{M}-prompt.md`，确认提示词 6 模块完整
3. 读取 `chapters/vol-{N}-ch-{M}.md` 确认 outline 和字数目标

## Step 2: 调子 agent 写作

1. 调用 `agents/pipeline/exec-prose.md`，传入卷号和章号
2. 子 agent 读提示词和章纲，按叙事段落顺序一次写完整章
3. 输出到 `archives/vol-{N}-ch-{M}-{slug}.draft.md`

## Step 3: 验证

| 检查项 | 操作 |
|--------|------|
| 输出文件存在？ | `archives/vol-{N}-ch-{M}-*.draft.md` 存在？不存在 → 重试或告知失败 |
| 字数达标？ | 正文字数 ≥ 章纲字数 80%？不足 → 标注具体缺口，问作者是否接受 |
| 目录正确？ | 写入到 archives/ 目录而非其他地方？ |

验证通过后告知作者正文已生成。

## 下一步

回到主流程，由主 SKILL.md 检测进度分发到验收+归档。
