---
name: novel
description: 人类与AI协作写小说的工作流系统。当用户提到"写小说""创建小说项目""讨论设定""设计角色""规划章节""写第X章""生成正文""归档""继续写""小说进度"时必须使用。即使只说"帮我写完""下一章怎么写"，也要先加载本技能判断当前进度和路由。
---

# Novel — 小说创作工作流

和 AI 一起写小说。从世界观搭建到正文写作，逐步推进。

**Core principle:** 必须按 Phase 顺序推进。跳过 Phase 等于让 subagent 在没有约束的情况下自行判断故事走向。

## The Iron Law

```
Phase 顺序不可跳。前置检查不可跳。STOP 点必须等作者确认。
```

如果你正在考虑跳过某步——停止。你没有选择权。

## When to Use

用户说"写小说""创建项目""讨论设定""设计角色""规划章节""写第X章""生成正文""归档""继续写""小说进度"等。

**When NOT to use:** 用户只是想聊小说内容、不需要系统化工作流。

## Anti-Patterns

| 借口 | 现实 |
|------|------|
| "作者说写第一章，我直接生成所有文件" | 必须按 Phase 顺序推进 |
| "差不多就行，不用那么详细" | 缺 memo，subagent 不知道读者在等什么 |
| "视角转换和变体一起生成效率更高" | 省一步就是省掉作者的控制权 |
| "模板我看懂了，直接帮作者填好" | Agent 引导讨论，不代笔填 YAML |

## The Process

### Step 1: 检测当前进度

读取项目根目录的 `story.yaml`。若不存在 → 项目未创建，路由到 `novel-setup`（Phase 1）。

若存在，读取最近操作的 `chapter.yaml`（按 `story.yaml` 的 chapters 列表找），判断：

| 信号 | 当前 Phase | 下一步 |
|------|-----------|--------|
| world-setting.yaml 字段大量为空 | Phase 2 未完成 | → `novel-setup` |
| chapter.yaml status = `outline`，memo 不完整 | Phase 3 进行中 | → `novel-outline` |
| chapter.yaml status = `outline`，memo 完整，segments 为空 | Phase 4 待执行——需拆 segment | → `novel-prompt` |
| chapter.yaml status = `outline`，segments 已填充，提示词不存在 | Phase 4 进行中——需生成提示词 | → `novel-prompt`（Step 0 展示已有 segments，确认后跳 Step 2） |
| chapter.yaml status = `draft`，正文未归档 | Phase 5/6 待执行 | → `novel-write` 或 `novel-archive`。建议归档前先 `novel-review` |
| chapter.yaml status = `archived` | 本章已完成 | 问作者：下一章还是回顾？可随时触发 `novel-review` 回顾评审 |

**章状态（chapter.status）:**
- `outline` — 章纲和情绪设计已确认，等待拆 segment → 生成提示词
- `draft` — segment 提示词已生成，正文写作/修改中，等待归档
- `archived` — 正文已归档

### Step 2: 匹配用户意图

| 用户说 | 目标 Phase | 子技能 |
|--------|-----------|--------|
| "创建项目""写小说""导入小说" | Phase 1 | `novel-setup` |
| "讨论设定""设计角色""世界观""写作风格" | Phase 2 | `novel-setup` |
| "规划章节""章纲""卷纲""故事线" | Phase 3 | `novel-outline` |
| "生成提示词""视角转换" | Phase 4 | `novel-prompt` |
| "写正文""写第X章""继续写""质量检查" | Phase 5 | `novel-write` |
| "归档""存档" | Phase 6 | `novel-archive` |
| "评审""评价""review""检查这章""这章怎么样" | 独立评审 | `novel-review` |
| "小说进度""第X卷进度" | 只读报告 | 本技能直接输出，不分发 |

### Step 3: 跳 Phase 检测

若目标 Phase > 当前 Phase + 1，检查前面 Phase 的产出是否完整：

- 目标 Phase 4 → 检查 chapter.yaml 的 memo 7 段是否填满、segments 是否已拆分
- 目标 Phase 5 → 检查 `prompts/vol-{N}-ch-{M}-seg-{1}-prompt.md` 是否存在
- 目标 Phase 6 → 检查正文是否已写入 archives/

缺失 → **STOP**。告知作者"XX 还没完成，先补这一环"，路由到前置 Phase 的子技能。

### Step 4: 分发

调用对应子技能。每个子技能遵循自己的流程，有自己的 STOP 点和确认步骤。

- `novel-setup`：Phase 1+2 — 初始化、世界观、角色、全局提示词
- `novel-outline`：Phase 3 — 卷纲、章纲、memo、情绪设计、卷提示词
- `novel-prompt`：Phase 4 — 叙事段落拆分、视角转换、per-segment 提示词生成
- `novel-write`：Phase 5 — 串行 subagent 写各段、拼接全文、质量检查+深度评审
- `novel-archive`：Phase 6 — 归档、角色更新、钩子更新、滑动窗口审视
- `novel-review`：Phase 5→6 推荐评审 — 10 维 60+ 细项诊断，对照全部设定文件逐条评审章正文

## 模型策略

各 Phase 根据任务性质使用不同模型。主 Agent 调用子技能时按此表选择模型，跳过模型参数则继承主会话当前模型。

| Phase | 子技能 | 推荐模型 | 原因 |
|-------|--------|---------|------|
| 1+2 | novel-setup | sonnet/opus | 世界观讨论、角色设计、风格确认——需要深度思考 |
| 3 | novel-outline | sonnet/opus | 章纲规划、情绪设计、结构推理 |
| 4 | novel-prompt | sonnet/opus | 视角转换、segment 拆分、提示词组装——最耗推理 |
| 5 | novel-write (subagent) | haiku | 正文生成，大量 serical 调用——快省优先 |
| 6 | novel-archive | haiku | 归档、状态更新——机械操作 |
| review | novel-review | sonnet/opus | 深度评审需要批判性思考 |

**说明：**
- Claude Code: `haiku` = deepseek-v4-flash
- OpenClaw / Hermes: 不传模型参数，使用平台默认模型
- 每个子技能的 SKILL.md 中 Agent() 调用的 `model` 参数由具体实现读取（如 Phase 5 从 `writing-style.yaml` 的 `writing_model` 读取）

## 授权模式

- **步步授权（默认）**：每步需作者确认
- **全部授权**：Agent 全权决定

作者随时说"你全权决定"或"每步都要我确认"切换。子技能继承此模式。

## Bundled Resources

| 路径 | 用途 | 何时读取 |
|------|------|---------|
| `scripts/init.py` | 创建项目骨架 | Phase 1 新建项目时执行 |
| `scripts/import.py` | 导入已有小说，切分章节 | Phase 1 导入模式时执行 |
| `scripts/templates/` | YAML 模板（world-setting、character、writing-style、hooks 等） | 新建项目时 init.py 自动复制；Phase 2 讨论设定时参考字段结构 |
