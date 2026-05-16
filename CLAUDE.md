# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is **awesome-novel-skilll** — a state-driven AI collaborative novel writing workflow system. It guides authors through world-building, character development, story outlining, and chapter writing using AI agents.

The system is designed for multiple AI tools (DeepSeek TUI, Claude Code, Hermes, OpenClaw) and primarily uses Chinese.

**完整流程、架构、子技能、文件约定见 SKILL.md。**

---

## Skill 强制执行规则

### 核心原则

**Skill 是唯一入口。没有例外。**

任何对项目文件的读写操作（设定/章纲/提示词/正文/状态），必须通过对应 skill 执行。主 Agent 直接操作项目文件 = 违规。

### 判定标准

以下情况必须调用 Skill 工具：

| 触发条件 | 必须调用的 skill |
|----------|------------------|
| 用户说"创建项目"、"写小说"、"开始设定" | `Skill: awesome-novel` |
| 用户说"规划卷纲"、"下一卷" | `Skill: awesome-novel` |
| 用户说"规划章节"、"这章写什么" | `Skill: awesome-novel` |
| 用户说"写正文"、"继续写" | `Skill: awesome-novel` |
| 用户说"验收"、"检查质量" | `Skill: awesome-novel` |
| 用户说"归档"、"存档" | `Skill: awesome-novel` |
| 用户说"评审"、"深度检查" | `Skill: awesome-novel` |
| 检测到 `chapter.md#status = outline`，无 prompt | 分发到 `skills/prompt/` |
| 检测到 `chapter.md#status = draft`，无草稿 | 分发到 `skills/write/` |
| 检测到 `chapter.md#status = draft`，有草稿 | 分发到 `skills/body-verify/` |

### 禁止的思维模式

- ❌ "这只是简单确认，跳过 skill" → 每次响应都要检查 skill 是否可用
- ❌ "用户好像很赶，直接做" → 流程不能压缩
- ❌ "结果看起来对，不需要走流程" → 正确的结果 ≠ 合规的过程
- ❌ "用户只问了一个问题" → 问题是否简单 与 是否需要 skill 无关
- ❌ "我认为不需要" → 没有主观判断空间

### 违规处理

如果跳过 skill 流程：

1. **立即承认** — "我跳过了 [具体步骤]，违规原因：[我的想法]"
2. **停止执行**
3. **通过 Skill 工具重新执行该步骤**
4. **报告给用户**

### 自检清单（每次响应前）

```
□ 我正要做什么操作？
□ 这个操作涉及项目文件吗？
□ 有对应的 skill 可以用吗？
□ 我是不是在用"理性"跳过某个步骤？
□ 用户的请求是否触发 awesome-novel skill？
```

如果任意问题回答"是"且我打算跳过 → 先调用 Skill。

### 唯一例外

主 Agent 读取以下文件**不需要**通过 skill：
- `.agent/status.md`（状态检测专用）
- `story.md`（版本检测专用）
- `chapters/vol-*-ch-*.md#status`（路由决策专用）

所有其他文件操作必须通过对应 skill。

---

## 产出检查规则

每个产出完成后，**必须先按对应指南自检 → 修复不合格项 → 再汇报**。

### 检查清单

| 产出 | 检查内容 | 验收规范 |
|------|----------|----------|
| 世界观设定 | 地理/政治/规则完整性 | `references/world-setup-style.md` |
| 写作风格 | 叙事身份/核心原则/描写技法 | `references/writing-style.md` |
| 题材设定 | 满足类型/节奏/禁忌配置 | `references/genre-style.md` |
| 角色设定 | 认知6层模型完整性 | `references/character-setting-style.md` |
| 主线拆纲 | 总主线/断点/分卷冲突 | `references/story-arc-style.md` |
| 卷纲 | 章节列表/因果链/章末变化 | `references/volume-setting-style.md` |
| 章纲 | memo 8段/情绪设计6字段/hooks | `references/chapter-setting-style.md` |
| 提示词 | 6模块完整性/风格注入 | `references/prompt-setting-style.md` |
| 正文 | 15项质量门禁/AI味检测 | `references/chapter-quality-checklist.md` |

### 检查方式

1. **读指南** — 先读 `references/对应指南.md`，理解验收标准
2. **逐项检查** — 按指南中的清单逐项核查，证据要落在原文
3. **修复** — 不合格项先修复，再进行下一步

### 铁律

- ❌ 边写边检查 → 应写完后统一检查
- ❌ 检查完直接汇报不修复 → 先修复再汇报
- ❌ 目测一遍就放行 → 必须逐项打勾

### 汇报格式

```
[产出] 已完成。
检查结论：X 项通过 / Y 项不合格
不合格项已修复：
- [修复项 1]
- [修复项 2]
```

---

## Critical Invariants

| 文件 | 约束 |
|------|------|
| `chapters/*.md#status` | 进度标记：`outline` \| `draft` \| `archived` |
| `archives/*.md` | 正文唯一存放处。`-draft` = 未归档 |
| `character-setting/*.md` | 追加写入，不覆盖 |

---

## NEVER / ALWAYS

**NEVER:**
- ❌ Git operations (commit, push, branch)
- ❌ Modify files outside the project directory
- ❌ Skip sub-skill dispatch
- ❌ Overwrite character files — append only

**ALWAYS:**
- ✅ Check `chapter.md#status` before deciding next action
- ✅ Update `.agent/status.md` after completing sub-skill tasks
- ✅ Use independent verification (body-verify, prompt-verify)

---

## Model Requirements

- **Phase 1-3 (setup/outline/chapter):** Requires strong reasoning (DeepSeek V4 / Claude Sonnet class)
- **Writing phase:** Can use weaker models, quality may vary
- If model is weak: refuse Phase 1-3 execution, prompt user to check model configuration

---

## References

详细指南在 `references/` 目录：
- `chapter-quality-checklist.md` — 正文验收
- `chapter-setting-style.md` — 章纲格式
- `character-setting-style.md` — 角色认知模型
- `genre-style.md` — 题材配置
- `world-setup-style.md` — 世界观结构
- `story-arc-style.md` — 主线拆纲方法
- `volume-setting-style.md` — 卷纲格式
- `prompt-setting-style.md` — 提示词组装
- `writing-style.md` — 写作风格