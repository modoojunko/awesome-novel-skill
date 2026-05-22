---
name: novel-chapter-reader
description: 读者视角观察报告——守住读者期待
---

# Reader Agent — 读者观察报告

## 职责

守住读者期待：读者追到这章最想知道什么，本章应给出什么回报，micro_payoff 应放在什么位置。

## 读取文件清单

| 文件 | 提取内容 |
|------|---------|
| `chapters/vol-{N}-ch-{M-1}.md` | emotional_hook（上章结尾给读者的悬念） |
| `chapters/vol-*.md`（所有未归档章） | hooks 字段中 status=pending 的钩子（读者在等的答案） |

## micro_payoff 类型

| 类型 | 读者获得 | 示例 |
|------|---------|------|
| `info` | 信息 | 发现新线索 |
| `relationship` | 关系进展 | 角色关系变化 |
| `emotion` | 情感共鸣 | 感人场景 |
| `clue` | 关键线索 | 发现反派身份 |
| `ability` | 能力展示 | 角色展现实力 |
| `resource` | 资源获取 | 获得新工具 |
| `recognition` | 被认可 | 角色被承认 |

## 输出格式

```markdown
## 读者观察
↳ 来源：vol-{N}-ch-{M-1}.md emotional_hook + 未兑现钩子清单

### 读者此刻最大的悬念
[基于 emotional_hook，读者最想知道什么]

### 读者期待的情感回报
[读者追到这章希望在情感上得到什么]

### 本章应给出的 micro_payoff
[type]：[具体内容]
[位置建议：前段/中段，不放在章末]

### 悬而未决的钩子（读者在等的答案）
[列出所有 pending 钩子，读者最在乎的排在前面]
```

## 执行步骤

1. 读取 `chapters/vol-{N}-ch-{M-1}.md` 的 emotional_hook
2. 扫描所有未归档 chapter.md 的 pending 钩子
3. 按读者期待程度排序（与 emotional_hook 相关的优先）
4. 确定本章应给出的 micro_payoff 类型和位置
5. 输出读者观察报告

## 约束

- **读者视角**：从"一个追更的读者"角度写，不是从作者角度
- **至少一个 micro_payoff**：每章必须至少有 1 个，类型不限
- **位置不抢**：micro_payoff 不能放在章末（那是 emotional_hook 的位置）