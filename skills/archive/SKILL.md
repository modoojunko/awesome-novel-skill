---
name: novel-archive
description: 章节归档与状态更新（参考文档，已内化到 chapter-loop）。正文审阅满意后归档——更新角色状态、情绪弧线、钩子追踪、滑动窗口审视。触发："归档""存档""这章完成了""满意了"。归档前必须先通过 Workflow 完整性检查，不完整章节拒绝归档。
---

> 参考文档——归档步骤已内化到 `skills/chapter-loop/SKILL.md` Step 5。此文件保留为详细操作参考，不再独立路由。

# Novel Archive — 归档

> 摘要：完整性检查 → 去 draft 标记 → 更新角色状态历史 + hooks → 卷完成检测 → 滑动审视。

## Overview

正文落盘后，更新项目状态——角色状态、情绪弧线、钩子、滑动审视。

**When NOT to use:** 正文未写入 archives/、质量检查未通过、章状态已是 archived。

**Announce at start:** "我来归档第{N}卷第{M}章。"

## 执行前提

归档前 read_file 执行 Step 0 完整性检查表。任意一项不通过 → 报告作者缺少哪项。

## 归档前完整性检查（Step 0）

| 检查项 | 操作 |
|--------|------|
| chapter.md 完整性 | memo（7段）+ emotional_design 全部有值？缺失 → Read `skills/chapter-loop/SKILL.md` Step 1 补全章纲 |
| 章提示词文件存在？ | `prompts/vol-{N}-ch-{M}-prompt.md` 存在？缺失 → 回 `skills/chapter-loop/SKILL.md` Step 2 自动生成 |
| 正文通过全部质量检查？ | 未通过 → 返回到 `skills/chapter-loop/SKILL.md` Step 3 修复 |
| 深度评审已完成？ | 建议归档前先触发 `novel-review`（10 维诊断），未评审 → 提醒作者可选评审 |

## 归档步骤

1. 将草稿文件重命名，去掉 `-draft` 标记：
   `archives/vol-{N}-ch-{M}-{slug}.draft.md` → `archives/vol-{N}-ch-{M}-{slug}.md`
2. 复核 archives/ 中归档文件内容无误
3. 分析角色变化，追加 `状态历史`
4. 更新角色 yaml 当前状态字段（位置、能力、关系、世界观、概要）
5. 追记 `情绪弧线`（情绪状态、触发事件、强度、弧线方向、表达方式）
6. 更新角色 yaml 中的 hooks 引用（全局 hooks.md 不再维护——真相源在各 chapter.md 的 hooks 字段），运行钩子健康检查
7. 运行情节推进停滞检测（最近 3 章是否有实质性推进）
8. 将 chapter.md status 更新为 `archived`
9. 更新 story.md chapters 列表
10. **滑动窗口审视**：
    - 以最近 3 章为窗口检查优先级、节奏意图、钩子是否仍然适用
    - 3 的倍数章（3/6/9…）→ 必须引导作者主动回顾方向
    - 状态不符 → 报告差异并建议调整
    - 状态一致 → 报告"无需调整"
11. **检测卷边界**：
    - 读 `chapters/` 目录，筛选当前卷的章节文件（`vol-{N}-ch-*.md`）
    - 检查这些章节的 status 是否全部为 `archived`
    - 未全部完成 → 不做额外操作
    - 全部完成 → **输出卷完成报告：**

      ```
      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        卷 {N} 《{title}》全部 {M} 章已完成
      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

      已归档章节：
      {逐章列出标题和归档状态}

      下一步选项：
      1. 规划卷 {N+1} — 进入 `novel-volume`，AI 推理方向选项
      2. 回顾整卷 — 触发 novel-review 做整卷回顾评审
      3. 修改某章 — 指定章节重新生成

      卷 {N+1} 的新故事从当前角色状态自然生长。建议先走选项 1——让 AI 推理方向选项——基于当前角色状态推导下一卷。
      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
      ```

## 状态历史格式

```yaml
状态历史:
  - 所在卷: 1
    所在章: 1
    位置: "角色当前位置"
    状态: "角色当前状态简述"
    变化:
      - "具体变化1"
```

## 情绪弧线格式

```yaml
emotional_arc:
  - volume: 1
    chapter: 1
    emotional_state: "愤怒/压抑/释然/期待/恐惧/温情/决心"
    trigger_event: "触发事件"
    intensity: 7
    arc_direction: "上升/回落/持平/转折"
    expression: "身体反应/行为/对话/环境互动"
```

## 下一步

归档完成后告知作者。根据滑动窗口审视结果提出下一章方向建议。

**卷边界时：** 步骤 11 检测到卷全部完成时，展示卷完成报告，路由选择：
- "规划下一卷" → 主 Agent Read `skills/outline/SKILL.md` 规划下一卷纲
- "回顾整卷" → Read `skills/review/SKILL.md` 做整卷评审
- "修改某章" → 指定章节，Read `skills/chapter-loop/SKILL.md` 重新生成
