# awesome-novel-skilll 架构文档

> 面向使用者理解工作流，面向开发者理解实现细节。

---

## 第一部分：使用者视角

### 1. 系统概览

**是什么：** 和 AI 一起写小说的工作流系统。从世界观搭建到角色塑造，从章节规划到正文写作，一步步陪你完成整部小说。

**核心流程：**
```
一次性设定 → 主线拆纲 + 卷纲展开 → 逐章写作循环
```

**逐章写作循环：**
```
章纲 → 提示词 → 提示词验收 → 正文 → 正文验收 → 归档 → 下一章
```

**状态驱动：** 系统根据当前进度自动路由下一步。你不需要记流程，Agent 会告诉你现在该做什么。

---

### 2. 工作流详解

#### Phase 1：一次性设定

第一次写小说时，Agent 和你聊这几个方面（不用一次性想好全部）：

| 方面 | 内容 |
|-----|------|
| 题材选择 | 仙侠、都市、悬疑、历史……Agent 按题材配置写作风格和节奏模板 |
| 世界观 | 故事发生在什么世界？有什么特殊规则？ |
| 主要角色 | 逐个讨论性格、能力、成长经历 |
| 写作风格 | 偏好更偏描写还是更偏对话？可以导入喜欢的小说提取文风 |

**预置题材画像：** 项目内置 24 套题材档案，选一个就能直接开始。

**从喜欢的小说里学文风：**
1. 把参考小说文件放进项目目录
2. 跟 Agent 说"分析一下这本小说的文风"
3. Agent 跑统计分析，输出风格档案
4. 确认后自动合并到写作配置

#### Phase 2：主线拆纲 + 卷纲展开

设定完成后，Agent 帮你规划整体故事结构：

1. **主线拆纲** — 一句话说清全书核心冲突，从结局倒推拆成几个大阶段
2. **分卷规划** — 每个阶段就是一卷，每卷大概写什么、到什么位置
3. **定第一卷章节** — 第一卷分几章，每章的核心内容

#### Phase 3：逐章写作循环

每章按这个流程走：

| 步骤 | 做什么 | 文件 |
|-----|-------|------|
| ① 章纲 | Agent 给出写作计划——写什么、分几段、情绪怎么走 | `chapters/vol-{N}-ch-{M}.md` |
| ② 提示词 | 根据章纲和全局设定自动组装写作提示词 | `prompts/vol-{N}-ch-{M}-prompt.md` |
| ③ 提示词验收 | 你审阅提示词，确认后进入写作 | — |
| ④ 写正文 | Agent 按提示词写完整一章 | `archives/vol-{N}-ch-{M}-{slug}.draft.md` |
| ⑤ 正文验收 | 你审阅正文，说"归档"或"改第X段" | — |
| ⑥ 归档 | 确认后这章正式存档，角色状态更新 | `archives/vol-{N}-ch-{M}-{slug}.md` |

**章完成后：** Agent 会问"下一章继续吗？"

---

### 3. 关键概念

#### 章状态生命周期

```
outline → draft → archived
```

| 状态 | 含义 |
|-----|------|
| `outline` | 章纲已生成，等待写提示词 |
| `draft` | 提示词验收通过，等待写正文 |
| `archived` | 正文归档完成 |

#### 动态记忆系统

记录作家反馈，让 Skill 越写越懂你：

**工作流程：**
```
生成草稿 → 保存 AI 原版 → 作家修改 → 归档时 diff 对比 → 追问确认 → 记录模式
```

**记录内容：**
- **反 AI 模式** — 识别 AI 常见套路，作家如何破解
- **作家文风** — 这个作家的表达偏好

**文件结构：**
```
{project}/
  .agent/                    # 临时文件（本章归档后清理）
    {chapter}-draft-ai.md    # AI 原版快照
    {chapter}-draft-diff.md   # diff 对比结果
  .memory/                   # 持久积累（作家私有）
    anti-ai.md               # 反 AI 模式
    writer-style.md          # 作家文风
```

**提示词注入：** 每次生成提示词时，读取 `.memory/` 全量 + `references/{genre}/defaults.md`，Agent 整合后注入。

**社区贡献：** 作家可说"贡献这个模式"，Skill 生成 community-ready 格式，引导提 PR。

#### 三种协作模式

| 模式 | 触发词 | 行为 |
|-----|--------|------|
| **步步确认**（默认） | — | 每做一步都等你点头才继续 |
| **全部授权** | "你全权决定" | 流程节点还在，Agent 代按确认 |
| **SOLO 模式** | "solo" / "单机" | 无 STOP 点，Agent 完成全部 |

---

## 第二部分：开发者视角

### 4. 系统架构

#### 状态驱动循环

核心架构是**状态驱动循环**，而非线性流水线：

```
Step 1（检测状态）→ 匹配路由 → Read 子skill → 执行子task → 更新状态 → 回到 Step 1
```

`chapter.md#status` 字段是路由决策的唯一依据。所有子 skill 读取此状态并在完成后更新它。

#### 主 Agent vs 子技能

| 角色 | 职责 |
|-----|------|
| **主 Agent（SKILL.md）** | 状态检测、分发路由、协调子技能 |
| **子技能（skills/*/）** | 各自负责一个具体环节的执行 |

#### 子技能分工

| 子技能 | 职责 | 触发条件 |
|--------|------|----------|
| `setup/` | 项目初始化 + 设定 | 新项目 |
| `outline/` | 主线拆纲 + 卷纲 | "规划卷纲"、"故事线" |
| `chapter/` | 章纲生成 | status=outline |
| `prompt/` | 提示词生成 | status=outline，无提示词 |
| `prompt-verify/` | 提示词验收 | status=outline，有提示词 |
| `write/` | 正文生成 | status=draft，无草稿 |
| `body-verify/` | 正文验收 | status=draft，有草稿 |
| `review/` | 深度评审 | 作者要求 |
| `archive/` | 归档 + 动态记忆 | 作者确认归档 |

---

### 5. 数据流

```
[设定阶段]
  story.md → settings/（world/character/writing/genre）

[卷纲阶段]
  story.md → volumes/volume-{N}.md

[章循环]
  chapter.md (status=outline) → prompt.md → verify → chapter.md (status=draft)
  → archives/*.draft.md → verify → archive
  → .agent/*-ai.md + .memory/*.md（动态记忆）
```

---

### 6. 文件结构

```
{project-name}/
├── story.md              # 项目索引（元信息/引用路径/主线拆纲）
├── settings/
│   ├── world-setting.md  # 世界观
│   ├── writing-style.md  # 写作风格
│   ├── genre-setting.md  # 题材设定
│   └── character-setting/
│       └── <id>.md       # 每角色一个（追加写入）
├── volumes/
│   └── volume-{N}.md     # 卷纲
├── chapters/
│   └── vol-{N}-ch-{M}.md # 章纲（status 驱动路由）
├── prompts/
│   └── vol-{N}-ch-{M}-prompt.md  # 提示词
├── archives/
│   ├── *.draft.md        # 草稿（写作中）
│   └── *.md              # 定稿（归档后）
├── .agent/               # 临时文件
│   ├── status.md         # Agent 状态追踪
│   └── {chapter}-draft-ai.md  # AI 原版快照
└── .memory/              # 持久记忆
    ├── anti-ai.md        # 反 AI 模式
    └── writer-style.md   # 作家文风
```

---

### 7. references/ 内容说明

```
references/
├── chapter-quality-checklist.md  # 正文验收清单（15项）
├── chapter-setting-style.md      # 章纲格式 + 情绪设计
├── character-setting-style.md    # 角色认知6层模型
├── genre-style.md               # 节奏规则/满足类型/禁忌
├── world-setup-style.md         # 地理/政治/规则结构
├── story-arc-style.md           # 主线拆纲方法论
├── volume-setting-style.md      # 卷纲格式
├── prompt-setting-style.md      # 提示词组装结构
├── writing-style.md             # 写作风格方法论
├── anti-ai/                    # 反 AI 规则库
│   ├── fanqie.md              # 反 AI 规则学习库
│   ├── common-rules.md         # 通用反 AI 规则
│   └── {genre}/defaults.md     # 题材反 AI 默认模式
├── writer-style/              # 作家文风参考
│   └── {genre}/defaults.md     # 题材文风默认参考
└── genre-example/              # 填充案例（按题材）
```

---

### 8. 扩展点

#### 贡献社区 defaults

1. 作家在 `.memory/` 积累自己的模式
2. 说"贡献这个模式"
3. Skill 生成 community-ready 格式
4. 引导作家提 PR 到 `references/`

#### 新增题材类型

1. 在 `references/genre-example/` 添加题材填充案例
2. 在 `references/anti-ai/{genre}/defaults.md` 添加反 AI 默认模式
3. 在 `references/writer-style/{genre}/defaults.md` 添加文风参考

---

### 9. 关键约束

- **chapters/*.md#status** — 进度标记，`outline → draft → archived`
- **archives/*.md** — 正文唯一存放处，有 `-draft` = 未归档
- **.memory/*.md** — 追加写入，不覆盖
- **.agent/*.md** — 临时文件，章归档后清理
- 作家本地记录优先于 references defaults