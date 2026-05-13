---
name: novel-body-verify
description: 正文验收——检查草稿是否符合 10 维质量标准。触发：主流程检测到 draft + archives 有草稿时自动分发。
---

# Novel Body Verify — 正文验收

> 读 `references/chapter-quality-checklist.md` 逐项检查。展示报告给作者确认。

## 工具契约

| 工具 | 用途 | 限制 |
|------|------|------|
| Read | 读正文草稿、chapter.md 章纲、prompt.md、章节质量 checklist | — |
| Write/Edit | 不写文件（只出报告） | — |
| Agent | 可选：开独立检查助手执行 10 维验收 | 助手只用 Read，不可写文件 |

## 错误恢复

| 失败场景 | 恢复策略 |
|---------|---------|
| 草稿文件格式异常（非 utf-8/空内容） | 报告作者"草稿不可读"，列出异常详情，不继续检查 |
| L1-L3 某层全部不可检 | 标记该层为 N/A，在报告中注明原因，不阻断其他层 |
| 作者要求修改时清单缺失 | 标记问题根因（prompt/章纲/风格参考），不自行修改 |

## 执行前提

| 检查项 | 操作 |
|--------|------|
| 草稿存在 | `archives/vol-{N}-ch-{M}-*.draft.md` 不存在 → **STOP** |
| 章纲存在 | `chapters/vol-{N}-ch-{M}.md` 存在且 memo 非空 |

## 验收步骤

1. 读 `references/chapter-quality-checklist.md`，按 10 维分层执行：

   **L1 表层文本：**
   - 疲劳词检查（6 大类阈值）
   - 句式违规检查（8 种结构癖好 + 6 种句式规则）
   - 对话规则检查（标签/间隔/意图/感叹号）

   **L2 内容合规：**
   - 设定合规（世界观/OOC/禁忌/连续性）
   - 章纲兑现（required_changes/payoff/prohibitions）
   - 钩子兑现（新埋/收束/分量）

   **L3+ 基础质量：**
   - 阅读留存（爽点 + 曲线 + 章末牵引力 + 获得感）
   - 基础质量（视角/时态/段落/内容质量/风格/字数）

2. 组装分层验收报告
3. 展示给作者确认
## 下一步

**状态汇报 + 自动路由：**
- ✅ 正文验收通过（作者确认）
- 📝 正文草稿已通过验收：`archives/vol-{N}-ch-{M}-{slug}.draft.md`
- → 主流程检测到 `status=draft` + 验收通过，**分发到归档**（`skills/archive/SKILL.md`）

**作者选择：**
- "进入归档" → 分发到归档
- "先做深度评审" → 分发到 `skills/review/SKILL.md`，评审后仍回归档

## 验收报告格式

见 `references/chapter-quality-checklist.md` §验收报告格式。
