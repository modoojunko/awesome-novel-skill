---
name: novel-archive
description: 章节归档与状态更新。Phase 6。正文审阅满意后归档——更新角色状态、情绪弧线、钩子追踪、卷提示词、滑动窗口审视 current-focus。触发："归档""存档""这章完成了""满意了"。归档前必须先通过 Workflow 完整性检查，不完整章节拒绝归档。
---

# Novel Archive — 归档

## Overview

正文落盘后，更新项目状态——角色状态、情绪弧线、钩子、卷提示词、current-focus 滑动审视。

**When NOT to use:** 正文未写入 archives/、质量检查未通过、章状态已是 archived。

**Announce at start:** "我来归档第{N}卷第{M}章。"

## HARD-GATE

```
归档前必须通过 Workflow 完整性检查。任意一项不通过 → STOP，修复后再归档。
```

## 归档前完整性检查（Step 0）

| 检查项 | 操作 |
|--------|------|
| chapter.yaml 完整性 | memo（7段）+ emotional_design 全部有值？缺失 → 退回 `novel-outline` |
| `prompts/vol-{N}-ch-{M}-prompt.md` 存在？ | 不存在 → 退回 `novel-prompt` |
| 提示词覆盖所有 key_points？ | 对照 outline.key_points。缺失 → 退回 `novel-prompt` |
| 正文通过全部质量检查？ | 未通过 → 退回 `novel-write` |
| 深度评审已完成？ | 建议归档前先触发 `novel-review`（10 维诊断），未评审 → 提醒作者可选评审 |

## 归档步骤

1. 复核 archives/ 中归档文件内容无误
2. 分析角色变化，追加 state_history
3. 更新角色 yaml 当前状态字段（location、abilities、relationships、worldview、summary）
4. 追记 emotional_arc（情绪状态、触发事件、强度、弧线方向、表达方式）
5. 更新 hooks.yaml（mention/resolve/defer），运行钩子健康检查
6. 运行情节推进停滞检测（最近 3 章是否有实质性推进）
7. 将 chapter.yaml status 更新为 `archived`
8. 更新 story.yaml chapters 列表
9. **更新卷提示词**：往 `prompts/volume-{N}-prompt.md` 追加本章一句话摘要
10. **滑动窗口审视 current-focus.md**：
    - 标记本章为 ✅
    - 以最近 3 章为窗口检查优先级、节奏意图、钩子是否仍然适用
    - 3 的倍数章（3/6/9…）→ 必须引导作者主动更新
    - 状态不符 → 报告差异并建议更新
    - 状态一致 → 报告"无需更新"

## state_history 格式

```yaml
state_history:
  - after_volume: 1
    after_chapter: 1
    location: "角色当前位置"
    status: "角色当前状态简述"
    changes:
      - "具体变化1"
```

## emotional_arc 格式

```yaml
emotional_arc:
  - volume: 1
    chapter: 1
    emotional_state: "愤怒/压抑/释然/期待/恐惧/温情/决心"
    trigger_event: "触发事件"
    intensity: 7
    arc_direction: "rising/falling/holding/turning"
    expression: "身体反应/行为/对话/环境互动"
```

## 下一步

归档完成后告知作者。根据滑动窗口审视结果，建议下一章或调整 current-focus。
