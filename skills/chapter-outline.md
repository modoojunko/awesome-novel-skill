# 生成章纲 skill

校准后的参考材料 → 一份可执行的章纲。格式规范参考 `knowledge/format-specs/chapter-setting-style.md`。

## 流程

展开纲要点 → 禁止清单 → Chapter Memo 8段 → 情绪设计 → Hooks → 设变通知（可选）→ 产出

## 细化章纲

按 `chapter-setting-style.md` 的格式规范逐项填充。以下为执行顺序，具体格式和写法参考该规范：

**a. 展开纲要点** — 按 §二(从方向到纲要点) 的三段锚点法拆解，8-12 条 key_points。作者确认后进入下一步。

**a2. 禁止清单** — 按 §(不做什么——硬约束红线) 询问并记录 prohibitions。

**b. Chapter Memo 8段** — 按 §三(章纲内容清单) 的 7 段逐段填充：
1. current_task（当前任务）
2. reader_expectation（读者期待）
3. payoff_plan（兑现计划）
4. downtime_functions（过渡功能）
5. key_choices（关键抉择）
6. knowledge_state（角色信息状态）
7. required_changes（章尾改变）

填完后展示完整 memo 供作者确认。

**c. Emotional Design** — 按 §四(情绪设计) 填充：primary_mood、mood_progression、intensity_peak、intensity_level、emotional_hook、micro_payoffs。

**d. Hooks 操作** — 写入本章的钩子操作（埋/推进/收束）。不读写全局 hooks.md——真相源在各 chapter.md 的 hooks 字段。

**e. 设变通知（可选）** — 规划/校准过程中发现的设定变更需求。用于通知 novel-agent 调度 updater。按需在章纲末尾追加：

```
---
## 设定变更通知

- **目标：** settings/character-setting/{id}.md
- **类型：** 状态更新 / 新角色 / 世界观更新
- **原因：** {为什么需要这个变更}
- **详情：** {具体变更描述}
---
```

只在有变更时追加，无则省略。

## 产出

写入 `chapters/vol-{N}-ch-{M}.md`，status → `outline`
