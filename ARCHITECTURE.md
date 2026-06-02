# awesome-novel-skilll 架构文档

> 面向开发者理解实现细节。面向使用者的内容见 [README.md](./README.md)。

---

## 1. 系统架构

### 状态驱动循环

核心架构是**状态驱动循环**，而非线性流水线：

```
Step 1（检测状态）→ 匹配路由 → Read 子skill → 执行子task → 更新状态 → 回到 Step 1
```

`chapter.md#status` 字段是路由决策的唯一依据。所有子 skill 读取此状态并在完成后更新它。

### 主 Agent vs 子技能

| 角色 | 职责 |
|-----|------|
| **主 Agent（SKILL.md）** | 状态检测、分发路由、协调子技能 |
| **子技能（skills/*/）** | 各自负责一个具体环节的执行 |

### 子技能分工

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

## 2. 数据流

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

## 3. 文件结构

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

## 4. knowledge/ 与 memory/ 内容说明

```
knowledge/                   # 静态参考知识（→ 项目 .claude/knowledge/）
├── format-specs/            # 格式规范
│   ├── chapter-quality-checklist.md  # 正文验收清单（15项）
│   ├── chapter-setting-style.md      # 章纲格式 + 情绪设计
│   ├── character-setting-style.md    # 角色认知6层模型
│   ├── genre-style.md               # 节奏规则/满足类型/禁忌
│   ├── world-setup-style.md         # 地理/政治/规则结构
│   ├── story-arc-style.md           # 主线拆纲方法论
│   ├── volume-setting-style.md      # 卷纲格式
│   ├── prompt-setting-style.md      # 提示词组装结构
│   └── writing-style.md             # 写作风格方法论
└── genre-example/           # 填充案例（按题材）

memory/                      # 动态记忆参考（→ 项目 .claude/memory/）
└── anti-ai/                 # 反 AI 规则库
    ├── common-rules.md      # 通用反 AI 规则
    └── {genre}.md           # 题材反 AI 默认模式
```

---

## 5. 动态记忆系统

### 工作流程

```
生成草稿 → 保存 AI 原版到 .agent/ → 作家修改 → 归档时 diff 对比 → 追问确认 → 语义合并 → 记录到 .memory/
```

### 文件职责

| 文件 | 时效 | 管理方 |
|-----|------|------|
| `.agent/{chapter}-draft-ai.md` | 临时，本章归档后删除 | Skill 自动 |
| `.agent/{chapter}-draft-diff.md` | 临时，回顾完成后删除 | Skill 自动 |
| `.memory/anti-ai.md` | 持久，积累反 AI 模式 | 作家私有 |
| `.memory/writer-style.md` | 持久，积累作家文风 | 作家私有 |

### 语义合并规则

1. **完全相同** → 跳过，告知作家"已存在"
2. **语义重复** → 合并为一条，用更好的表述
3. **场景重叠** → 扩展已有条目的场景范围
4. **冲突** → 询问作家确认

### 提示词注入

每次生成提示词时：
1. 读取 `{project}/.claude/memory/anti-ai.md`
2. 读取 `{project}/.claude/memory/writer-style.md`
3. 读取 `memory/anti-ai/{genre}.md`
4. 读取 `memory/anti-ai/common-rules.md`
5. Agent 语义去重、合并冲突、提炼规则
6. 标注来源 `[作家偏好]` / `[社区defaults]`，注入提示词"写作风格"部分

### 社区贡献

1. 作家说"贡献这个模式"
2. Skill 读取 `.memory/`，提取适合社区的条目
3. 生成 community-ready 格式
4. 引导作家提 PR 到 `memory/anti-ai/` 或 `knowledge/`

---

## 6. 扩展点

### 贡献社区 defaults

1. 作家在 `.claude/memory/` 积累自己的模式
2. 说"贡献这个模式"
3. Skill 生成 community-ready 格式
4. 引导作家提 PR 到 `memory/anti-ai/` 或 `knowledge/`

### 新增题材类型

1. 在 `knowledge/genre-example/` 添加题材填充案例
2. 在 `memory/anti-ai/` 添加反 AI 默认模式
3. 在 `memory/writer-style/` 添加文风参考

---

## 7. 关键约束

- **chapters/*.md#status** — 进度标记，`outline → draft → archived`
- **archives/*.md** — 正文唯一存放处，有 `-draft` = 未归档
- **.memory/*.md** — 追加写入，不覆盖
- **.agent/*.md** — 临时文件，章归档后清理
- 作家本地记录优先于 references defaults