# Multi-Agent Architecture Design

## Overview

将 awesome-novel skill 从"单 Agent 一体化工作流"重构为"多 Agent 协作系统"——主 Agent 纯决策，子 Agent 纯执行/验收/讨论，职责完全隔离。

---

## 1. Architecture Philosophy

### 三个角色

```
作者 ─── 主Agent（pro级模型，决策+流程）
          │
          ├── 圆桌模式（设定 + 章纲）
          │   └── 多个讨论agent（flash级模型），各司其职碰撞
          │
          └── 流水线模式（提示词 + 正文 + 归档）
              ├── 执行agent（flash级模型，干活）
              ├── 验收agent（flash级模型，挑刺）
              └── 去AI味agent（flash级模型，润色）
```

### 核心原则

- **职责隔离**: 每个 agent 只做一件事，不知道其他 agent 的存在
- **输入即契约**: 主 Agent 塞给子 Agent 的 prompt 就是全部授权范围
- **验收独立**: 执行和验收是不同角色，避免"自己写自己审"
- **无状态**: 每个子 Agent 用完即消失，不保留记忆
- **决策归一**: 所有"怎么办"都回到主 Agent，不会出现多 agent 互相扯皮
- **可熔断**: 主 Agent 设重试上限，超限降级或标记

---

## 2. 主 Agent（项目经理 + 仲裁者）

### 定位

不参与任何实际创作、验收、修改工作。只做决策。

### 职责

| 角色 | 职责 | 决策示例 |
|------|------|---------|
| **项目经理** | 拆解作者目标、调度资源、跟踪进度、汇报 | "今天写完卷1" → 评估剩余工作量，排优先级 |
| **仲裁者** | 验收不通过时判断责任方，边界不清时升级 | 执行的问题→派执行修；验收误报→跳过；两难→升级作者 |

### 模型要求

- **pro 级模型**（deepseekv4-pro / 同级别）
- 原因：需要拆解模糊目标、评估风险、做判断决策

### 行为模式

```
接到作者目标 → ① 评估当前进度与目标差距
              → ② 决策下一步：派谁？给什么输入？要什么产出？
              → ③ 派活 → 等结果
              → ④ 判断结果：
                   成功 → 进入下一步 / 汇报
                   失败 → 判断谁的问题 → 派对应人修 → 同一人复验
                   循环超限 → 降级（夜间） / 升级（白天）
```

### 不做清单

- 不讨论设定
- 不写章纲
- 不写正文
- 不验收
- 不改文

---

## 3. 子 Agent 类型

### 3.1 模型规格

- **flash 级模型**（deepseekv4-flash / 同级别）
- 执行明确指令，不自己做决策

### 3.2 两种工作模式

#### 圆桌模式（设定 + 卷纲 + 章纲）

多角色从各自角度碰撞讨论，产出方案。

特点：
- 每个 agent 有独立视角和关注点
- 互相 critique 和补充
- 收敛到一致方案后输出

#### 流水线模式（提示词 + 正文 + 归档）

单一 agent 按指令产出 → 验收 agent 检查 → 循环。

特点：
- 执行 agent 写 → 验收 agent 检 → 主 Agent 判结果
- 不通过 → 同一执行修 → 同一验收复验
- 循环直到通过或触发熔断

---

## 4. 全阶段 Agent 清单

### Step 1 初始化

流程：主 Agent 先向作者收集最小信息，再派执行-初始化。

**主 Agent 收集的信息（5项）：**

| 字段 | 说明 | 例 |
|------|------|----|
| 书名 | 项目名称 | 凌晨6：47 |
| 目标读者 | 男频 / 女频 | 男频 |
| 题材/标签 | 题材分类 | 科幻末世 |
| 主角名 | 主要角色名 | 林默、林悦 |
| 作品简介 | 200字以内故事介绍 | 平凡都市青年意外获得... |

**主 Agent 追问示例：**
```
作者: "我想写本小说"
主Agent: "书名是什么？目标读者男频还是女频？
          什么题材？主角叫什么？
          写个200字的作品简介？"
```

信息收齐后派活：

| Agent | 类型 | 职责 | 输入 | 产出 |
|-------|------|------|------|------|
| 执行-初始化 | 流水线 | 根据5项信息建目录结构、填充初始 story.yaml | 书名/读者/题材/主角/简介 | 项目目录 + story.yaml |
| 验收-初始化 | 流水线 | 检查目录完整性、字段齐全 | 项目目录 | 验收报告 |

### Step 2 设定圆桌

参与者：作者（全程在场）+ 以下 agent

| Agent | 视角 | 关注点 |
|-------|------|--------|
| 地理师 | 世界物理层 | 大陆格局、气候、资源分布、地理对文明的影响 |
| 政治师 | 权力结构 | 国家关系、法律制度、权力交接、势力分布 |
| 文化师 | 社会生活 | 宗教信仰、社会习俗、日常生活、文化冲突 |
| 力量体系师 | 规则层 | 魔法/超自然/科技的规则、边界、代价 |
| 角色师 | 人物层 | 谁在这个世界里、动机、关系、世界观塑造的人格 |

产出：world-setting.yaml / character/*.yaml / writing-style.yaml / hooks.yaml

验收：独立的验收-设定 agent 检查内部一致性

### Step 3.1 卷纲圆桌

宏观：一卷的整体骨架。作者可选参与。

| Agent | 视角 | 关注点 |
|-------|------|--------|
| 结构师（宏观） | 全卷骨架 | 分几章、起承转合位置、高潮在哪一章、篇幅分配 |
| 主题师 | 主题递进 | 这卷的核心主题是什么、主题在章节间如何深化/转折 |
| 人物弧线师 | 角色成长线 | 角色在这卷的成长主线是什么、跨卷伏笔的锚点 |
| 钩子规划师 | 全卷悬念链 | 全卷钩子链设计、悬念锚点在哪、哪些钩子跨卷 |
| 节奏师 | 节奏图谱 | 这卷的松紧分布、密集区/舒缓区的交替 |

产出：volume.yaml（卷拆分 + 每卷的卷纲）

### Step 3.2 章纲圆桌

微观：每章的具体走法。作者可选参与。

| Agent | 视角 | 关注点 |
|-------|------|--------|
| 结构师（微观） | 章内结构 | 本章叙事结构、章内起承转合、倒叙/插叙等手法 |
| 人物驱动师 | 角色弧光 | 本章谁的主视角、角色动机推动情节而非被推 |
| 钩子管理师 | 本章钩子 | 本章埋/提/收哪些钩子、前后钩子逻辑链 |
| 情绪设计师 | 读者体验 | 本章情绪曲线（紧张/松弛/压抑/释放）、读者感受 |
| 设定守门员 | 边界检查 | 本章情节是否越设定边界、角色能力是否超纲 |

产出：chapter.yaml（章纲 + memo 7段 + 情绪设计 + 故事来龙去脉）

### Step 4 提示词

| Agent | 类型 | 职责 | 产出 |
|-------|------|------|------|
| 执行-提示词 | 流水线 | 拆 segment → 视角转换 → 组装提示词 | prompts/*.md |
| 验收-提示词 | 流水线 | 检查风格注入、视角转换彻底性 | 验收报告 |

### Step 5 写正文

| Agent | 类型 | 职责 | 产出 |
|-------|------|------|------|
| 执行-正文（并行） | 流水线 | 写 segment（每段一个实例并行） | segment 草稿 |
| 执行-缝合 | 流水线 | 合并多 segment 为一章 | 完整章草稿 |
| 验收-正文 | 流水线 | 6项检查（章纲一致/不吃设定/疲劳词/句式/对话/分段） | 验收报告 |
| 执行-去AI味 | 流水线 | 按 anti-ai.yaml 规则清理 AI 味 | 清理后正文 + 清理报告 |

清理后再验 → 同一验收-正文 agent 复验。

### Step 6 归档

| Agent | 类型 | 职责 | 产出 |
|-------|------|------|------|
| 执行-归档 | 流水线 | 更新角色 state / hooks / story.yaml / 去 draft 后缀 | 更新后的文件 |
| 验收-归档 | 流水线 | 检查角色状态与正文一致、钩子状态正确 | 验收报告 |

---

## 5. 流水线范式：执行 → 验收 → 循环

```
主Agent → 执行agent → 交付物
         │
         ▼
主Agent → 验收agent → 验收报告
         │
         ├── ✅ 通过 → 进入下一步 / 汇报
         │
         └── ❌ 不通过
                  │
                  ▼
            主Agent 判断:
            ├── 执行的问题 → 派同一执行agent修
            ├── 验收误报   → 跳过，标记问题但通过
            └── 两难       → 升级给作者（白天）/ 标记（夜间）
                  │
                  ▼
            同一验收agent复验 ←┘（循环直到通过或触发熔断）
```

### 熔断规则

| 场景 | 白天模式 | 夜间模式 |
|------|---------|---------|
| 执行失败第1次 | 调 prompt 重试 | 调 prompt 重试 |
| 执行失败第2次 | 换角度重构 prompt 重试 | 换执行 agent 重试 |
| 执行失败第3次 | 升级给作者决策 | 降低验收标准，标记问题继续 |
| 验收过严 | 主Agent 仲裁，放宽标准 | 主Agent 仲裁，放宽标准 |
| 验收过松 | 提高标准复验 | 标记"建议日间复审" |

---

## 6. 日间模式 vs 夜间模式

### 日间模式

- 作者在线，可随时决策
- 验收不通过 → 3 次重试 → 升级给作者
- 作者参与设定讨论、确认章纲、审阅正文

### 夜间模式

- 作者离线，不升级任何问题
- 验收不通过 → 3 次重试 → 降级通过并标记问题
- 设定/章纲未完成 → 不可自动执行（需要作者决策）
- 产出全程标记"夜间生成，请复审"

### 前置条件（夜间可自动执行）

- [ ] 设定已定稿（world-setting / character / writing-style / hooks）
- [ ] 章纲已确认
- [ ] 目标明确（如"今晚写完卷1"）

---

## 7. 文件组织

```
~/.claude/skills/awesome-novel/
├── SKILL.md                    # 主入口：流程定义 + 主Agent行为
├── agents/                     # 子Agent定义
│   ├── index.md               # Agent 索引清单（主Agent据此选人）
│   │
│   ├── roundtable/            # 圆桌模式 agent
│   │   ├── setting/          # 设定圆桌
│   │   │   ├── geographer.md
│   │   │   ├── politician.md
│   │   │   ├── culturist.md
│   │   │   ├── power-system.md
│   │   │   └── character-designer.md
│   │   ├── volume-outline/   # 卷纲圆桌
│   │   │   ├── structure.md
│   │   │   ├── theme.md
│   │   │   ├── character-arc.md
│   │   │   ├── hook-planner.md
│   │   │   └── pace.md
│   │   └── chapter-outline/  # 章纲圆桌
│   │       ├── structure.md
│   │       ├── character-driver.md
│   │       ├── hook-manager.md
│   │       ├── emotion-designer.md
│   │       └── setting-guardian.md
│   │
│   └── pipeline/             # 流水线模式 agent
│       ├── exec-init.md
│       ├── exec-world.md
│       ├── exec-character.md
│       ├── exec-style.md
│       ├── exec-hook.md
│       ├── exec-prompt.md
│       ├── exec-prose.md
│       ├── exec-stitch.md
│       ├── exec-de-ai.md
│       ├── exec-archive.md
│       ├── review-init.md
│       ├── review-setting.md
│       ├── review-prompt.md
│       ├── review-prose.md
│       └── review-archive.md
│
├── scripts/                   # 工具脚本
│   ├── init.py
│   ├── import.py
│   └── analyze_style.py
│
└── templates/                 # YAML/MD 模板
    ├── story.yaml.template
    ├── world-setting.yaml.template
    ├── writing-style.yaml.template
    ├── anti-ai.yaml.template
    ├── hooks.yaml.template
    ├── character.yaml.template
    ├── volume.yaml.template
    ├── chapter.yaml.template
    ├── author-intent.md.template
    └── current-focus.md.template
```

---

## 8. 主Agent 决策流程（伪代码）

```
主Agent::run(author_goal):
  # 1. 评估当前状态
  progress = read_story_yaml()
  gap = evaluate_gap(progress, author_goal)

  # 2. 检查前置条件
  if not prerequisites_met(gap.next_step):
    return "缺少前置条件: " + what_missing()

  # 3. 决定派谁
  agent = select_agent(gap.next_step)

  # 4. 组装上下文
  context = assemble_context(agent, progress)

  # 5. 如果是夜间模式，注入降级规则
  if is_night_mode():
    context.inject_fallback_rules()

  # 6. 派发 + 等待
  result = dispatch(agent, context)

  # 7. 判断结果
  if result.status == SUCCESS:
    update_progress(result)
    report_to_author(result.summary)
  elif result.status == FAILURE:
    # 仲裁逻辑
    if is_executor_fault(result):
      retry_or_escalate(result)
    elif is_reviewer_fault(result):
      override_and_proceed(result)
    else:
      escalate_to_author(result)
```

---

## 9. 关键边界

| 边界 | 规则 |
|------|------|
| 文件职责 | chapters/只放章纲，prompts/只放提示词，archives/只放正文 |
| 讨论产出 | 圆桌讨论收敛后才写入文件，不写中间态 |
| 夜间降级 | 3 次重试不过即降级，不卡流程 |
| 避不开的决策 | 设定方向、章纲方向、设定与正文冲突 → 必须升级作者 |
| 子 Agent 无记忆 | 每次调用都是全新实例，输入即全部上下文 |
