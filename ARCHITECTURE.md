# awesome-novel-skill 架构文档

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
| **主 Agent（novel-agent）** | 顶层入口，通过 `@novel-agent` 加载进主 AI。检测状态、写 order 文件、通过 Agent 工具调度子 agent。**不直接代劳子 agent 的工作** |
| **子 Agent（volume-planner / chapter-planner / prompt-crafter / writer / reader / updater）** | 各自负责一个具体环节的执行，由 novel-agent 调度，完成后清理 order 文件 |

### Agent 分工

| Agent | 职责 | 由谁调度 |
|-------|------|----------|
| `volume-planner` | 主线拆纲 + 卷纲规划 | novel-agent |
| `chapter-planner` | 章纲生成（memo + 情绪设计 + hooks） | novel-agent |
| `prompt-crafter` | 9 层提示词组装 | novel-agent |
| `writer` | 正文生成 + AI 味自检 | novel-agent |
| `reader` | 10 维 60+ 细项深度评审 | novel-agent（可选） |
| `updater` | 归档 + lore-keeping + 设定变更 | novel-agent |

---

### 调度架构

```
主 AI（加载 @novel-agent）
  │
  ├── 读 status.md → 判断当前 phase
  ├── 写 order 文件到 .agent/task/{type}-order.md
  ├── 通过 Agent 工具调度子 agent
  │     ├── volume-planner / chapter-planner（outline）
  │     ├── prompt-crafter / writer（draft）
  │     ├── reader（review，可选）
  │     └── updater（archive / setting-update）
  ├── 子 agent 完成后清理 order 文件
  └── 检测到 order 清理 → 推进下一阶段
```

**要点：** novel-agent 不直接写内容文件，只写 order 文件。子 agent 通过 Agent 工具调用，独立完成任务。

---

## 2. 数据流

```
[设定阶段]
  story.md → settings/（world/character/writing/genre）

[卷纲阶段]（四维方法论）
  story.md → volumes/volume-{N}.md
  ├─ 情绪走向：整卷情绪变化弧线（压抑→压抑→提升→打脸→装逼）
  ├─ 冲突阶梯：2-4 层逐级升高的障碍，每层间有转折点
  ├─ 信息差：卷定义起点→终点（开始时谁↦谁知道什么不知道什么，结束时谁知道了新信息）
  └─ 场景卡：每章三要素（主角想干啥+拦着他+悬念）

[章循环]（卷→章继承 + 章内小递推）
  chapter.md 继承卷的情绪位置/冲突层位/信息差弧段
  ├─ 章内微弧线：从卷走向的当前位置衍生
  ├─ 章内小阶梯：试探→遭遇→升级，每步比前一步难
  ├─ 章内信息差变化：设→用→揭→新信息差
  └─ 场景卡细化：三段锚点法（感官+动作+判断）

  chapter.md (status=outline) → prompt.md → verify → chapter.md (status=draft)
  → archives/*.draft.md → verify → archive
  → .agent/*-ai.md + .claude/memory/*.md（动态记忆，updater 归档时合并）
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
│   ├── task/             # 子 agent order 文件
│   └── {chapter}-draft-ai.md  # AI 原版快照
├── .claude/
│   ├── memory/           # 写作记忆（agent 实时记录 + updater 兜底）
│   │   ├── volume-memory.md    # 卷纲环节反馈
│   │   ├── chapter-memory.md   # 章纲环节反馈
│   │   ├── prompt-memory.md    # 提示词环节反馈
│   │   └── writing-memory.md   # 正文写作环节反馈
│   ├── knowledge/        # 静态知识（初始化时从 skill 仓库继承）
│   │   ├── anti-ai.md          # 反 AI 模式库
│   │   ├── writer-style.md     # 作家文风偏好
│   │   ├── permanent-memory.md # 永久记忆（从 memory/ 晋升的高频条目）
│   │   ├── format-specs/       # 格式规范
│   │   └── genre-example/      # 题材案例
│   └── agents/           # Agent 定义（初始化时从 agents/ 部署）
```

---

## 4. knowledge/ 与 memory/ 内容说明（Skill 仓库视角）

```
knowledge/                   # 静态参考知识 → 部署到项目 .claude/knowledge/
├── README.md               # 分层说明（自动注入 vs 与作者讨论）
├── format-specs/            # 格式规范
│   ├── chapter-quality-checklist.md  # 正文验收清单（15项）
│   ├── chapter-setting-style.md      # 章纲格式 + 情绪设计 + 章内冲突阶梯
│   ├── character-setting-style.md    # 角色认知6层模型 + 反派设定引用
│   ├── genre-style.md               # 节奏规则/满足类型/禁忌
│   ├── world-setup-style.md         # 地理/政治/规则结构
│   ├── story-arc-style.md           # 主线拆纲方法论（含冲突升级引用）
│   ├── volume-setting-style.md      # 卷纲格式 + 情绪走向/冲突阶梯/信息差/场景卡方法论
│   ├── prompt-setting-style.md      # 提示词组装结构（含驱动力/信息差/冲突阶梯层位/场景方法论注入）
│   ├── writing-style.md             # 写作风格方法论
│   └── memory-format-spec.md        # 记忆格式规范 + 生命周期
├── scene-craft/              # 场景写作方法论（经四步转化后注入输出·写作规范，AI 无需问作者）
│   ├── README.md            # 使用说明
│   ├── index.md             # 索引
│   ├── prose/               # 文笔技法（始终加载）
│   ├── pov/                 # 视角切换（始终加载）
│   ├── dialogue/            # 对话场景
│   │   ├── universal.md    #   通用
│   │   ├── xianxia.md      #   仙侠特化
│   │   └── suspense-crime.md # 悬疑特化
│   ├── fight/               # 战斗/对抗
│   │   ├── universal.md    #   通用（凡人级）
│   │   ├── xianxia.md      #   仙侠特化（超凡级）
│   │   └── suspense-crime.md # 悬疑特化
│   ├── appearance/          # 角色外貌描写（特殊条件触发）
│   ├── inner-mono/          # 心理活动/内心独白（特殊条件触发）
│   ├── death-scene/         # 角色死亡/下线（特殊条件触发）
│   ├── environment/         # 环境/氛围（待补充）
│   ├── group-scene/         # 群像场景（待补充）
│   └── transition/          # 过渡场景（待补充）
├── plot-craft/              # 剧情设计方法论（展示给作者讨论，不自动注入）
│   ├── README.md            # 使用说明
│   ├── index.md             # 目录（冲突升级/钩子/悲剧/情绪拉扯/开篇/反转）
│   ├── hook-techniques.md   # 钩子悬念
│   ├── tragedy-techniques.md # 悲剧虐心
│   ├── emotional-pull.md    # 情绪拉扯
│   ├── opening-hooks.md     # 开篇钩子
│   └── plot-twists.md       # 剧情反转
├── character-craft/         # 角色设定方法论（展示给作者讨论）
│   ├── villain-types.md     # 反派三大模板
├── title-craft/             # 取书名方法论（展示给作者讨论）
│   └── index.md
└── genre-example/           # 填充案例（按题材）

memory/                      # 静态参考素材 → 部署到项目 .claude/knowledge/
├── anti-ai/                 # 反 AI 规则库（→ anti-ai.md）
│   ├── common-rules.md      # 通用反 AI 规则
│   └── {genre}.md           # 题材反 AI 默认模式
└── writer-style/            # 文风参考（→ writer-style.md，可选）

项目 .claude/memory/ 下的动态记忆文件不在 Skill 仓库中，由 init.py 初始化为空桩，后续由 agent 在写作过程中填充。
```

---

## 5. 记忆系统

### 两级架构

```
┌────────────────────────────────────────────────────────────┐
│                    .claude/memory/                           │
│  动态记忆（各环节实时记录，updater 兜底维护）               │
│  ┌──────────────┐ ┌──────────────┐ ┌────────────────────┐  │
│  │volume-memory │ │chapter-memory│ │prompt-memory       │  │
│  │卷纲反馈       │ │章纲反馈       │ │提示词反馈           │  │
│  └──────────────┘ └──────────────┘ └────────────────────┘  │
│  ┌────────────────────┐                                     │
│  │writing-memory      │                                     │
│  │正文写作反馈        │                                     │
│  └────────────────────┘                                     │
└────────────────────────────────────────────────────────────┘
         │ use_count >= 4 晋升
         ▼
┌────────────────────────────────────────────────────────────┐
│              .claude/knowledge/permanent-memory.md           │
│  永久记忆（高频条目的沉淀，跨项目持久）                     │
│  连续 3 次 sweep 未使用 → 标记待移除 → 作者确认后删除      │
└────────────────────────────────────────────────────────────┘
```

### 工作流程

记忆捕获分两层，确保无遗漏：

```
第一层：agent 实时记录（写作过程中）
  agent 与作者讨论 → 作者反馈确认 → agent 识别可记录反馈
  → 追加到对应 memory 文件（volume/chapter/prompt/writing）
  → 递增已引用条目的 use_count

第二层：updater 兜底 sweep（agent 任务完成后）
  novel-agent 调度 updater → 读全部 memory 文件
  → 格式验证 → 查重 → 超 50 条压缩 → 晋升 / 降级永久记忆
  → 询问作者"还有要记的吗？"
```

### 条目生命周期

```
写入 memory/ → 被 agent 引用（use_count++）→ use_count >= 4
→ 晋升到 knowledge/permanent-memory.md（保留全部字段 + [promoted] 标记）
→ 后续写作周期持续引用 → 保留
→ 连续 3 次 sweep 未引用 → 展示给作者确认 → 删除
```

### 记录规则

- **原文**保留作者说法的关键词，不转写
- **结论**必须是可操作指引，不写空话
- **场景**描述触发条件，不写"卷纲讨论"这类泛词
- 同环节多次引用同一条目只计 1 次 use_count

### 语义合并（归档 diff）

归档时 updater 对比 AI 原版快照 vs 最终正文：

1. **完全相同** → 跳过
2. **语义重复** → 合并为一条，用更好的表述
3. **场景重叠** → 扩展已有条目的场景范围
4. **冲突** → 询问作家确认

语义合并结果写入 `.claude/knowledge/anti-ai.md` 和 `.claude/knowledge/writer-style.md`，标注 `[writer-preference]`。

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