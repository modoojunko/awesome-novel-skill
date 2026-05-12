---
name: novel-write
description: 正文生成——根据提示词写完整章正文。触发：提示词验收通过后自动分发，或手动"写正文""写这章"。完成后回到主流程。
---

# Novel Write — 正文生成

> 读 prompt → 调子 agent 写作 → 验证输出。主 Agent 做分发和验证，写作由子 agent 自主执行。

## Overview

提示词验收通过后，主 Agent 起一个子 agent 一次写完整章正文。主 Agent 不介入写作过程，只负责前置检查、分发和输出验证。子 agent 的写作指令内嵌在本文件中。

**When NOT to use:** prompt 文件不存在、chapter.md status 非 draft、本章正文已存在且未要求重写。

**Announce at start:** "我来调写作 agent 生成本章正文。"

## 执行前提

| 检查项 | 操作 |
|--------|------|
| prompt 文件存在？ | `prompts/vol-{N}-ch-{M}-prompt.md` 不存在 → **STOP**，返回主流程 |
| chapter.md status = draft？ | 非 draft → **STOP**，提示词尚未验收通过 |
| 正文已存在？ | `archives/vol-{N}-ch-{M}-*.draft.md` 已存在 → 问作者"覆盖还是继续编辑？" |

## Step 1: 准备

1. 确认卷号 `{N}` 和章号 `{M}`
2. 读取 `prompts/vol-{N}-ch-{M}-prompt.md`，确认 6 模块完整。字数目标和叙事视角从 prompt 模块 1 和模块 5 获取

## Step 2: 起子 agent 写作

启动子 agent（flash 模型），传入以下指令：

```
## Role
全章正文写作。只读提示词文件，一次性写完整章正文。章纲约束已全部注入提示词。

## Scope
- 做：读提示词，按叙事段落顺序写整章
- 不做：不读其他文件、不修改提示词、不写其他章、不写 settings/ 下任何文件

## Inputs
- `prompts/vol-{N}-ch-{M}-prompt.md` — 唯一输入（6 模块，含定位/承接/人物/场景/文字要求/真人感）

## Outputs
- `archives/vol-{N}-ch-{M}-{slug}.draft.md` — 全章正文草稿

## 写作规则
- 按提示词叙事段落 1 → N 顺序写，段落间过渡流畅
- 每个段落的写作指引必须兑现（场景/情绪/角色状态/结束画面）
- 结尾停在最后一段 ends_with 指定的画面或状态
- 正文不含解释、说明、引导语（不写"他感到""他意识到"）
- 字数不低于提示词模块 1 目标字数的 80%
```

子 agent 执行写完后返回。主 Agent 检查输出文件是否存在。

## Step 3: 验证

| 检查项 | 操作 |
|--------|------|
| 输出文件存在？ | `archives/vol-{N}-ch-{M}-*.draft.md` 存在？不存在 → 重试或告知失败 |
| 字数达标？ | 正文字数 ≥ 章纲字数 80%？不足 → 标注具体缺口，问作者是否接受 |
| 文件位置正确？ | 写入到 archives/ 目录而非其他地方？ |

验证通过后告知作者正文已就绪。

## 下一步

回到主流程，由主 SKILL.md 检测进度分发到验收+归档。
