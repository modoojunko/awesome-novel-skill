# 动态记忆系统设计

## 目标

记录作家审视和修改正文的反馈，提炼为：
1. **反AI模式** — 识别AI常见套路，作家如何破解
2. **作家文风** — 这个作家的表达偏好

这些记忆注入提示词，让 Skill 越写越懂作家。

## 核心流程

```
[生成草稿]
    ↓
Skill 保存 AI 原版 → .agent/{chapter}-draft-ai.md
    ↓ 作家修改
Skill 执行 diff → .agent/{chapter}-draft.diff.md
    ↓ 归档时追问
作家确认记录 → 写入 .memory/anti-ai.md / writer-style.md
    ↓
写新章时
Skill 读取 .memory/ + references/{genre}/defaults.md → Agent整合 → 注入提示词
```

## 文件结构

```
references/                                    # Skill 内置（社区共享）
  genre-example/                               # 填充案例
  anti-ai/
    fanqie.md                                  # 反AI规则库
    common-rules.md                            # 通用反AI规则
    {genre}/defaults.md                        # 各题材反AI默认模式
  writer-style/
    {genre}/defaults.md                        # 各题材文风参考

{project}/
  .agent/
    {chapter}-draft-ai.md      # AI原版快照（临时）
    {chapter}-draft.diff.md    # 对比结果（临时）
  .memory/
    anti-ai.md                 # 本项目反AI模式积累
    writer-style.md             # 本项目作家文风积累
```

## 各环节细节

### 1. AI 原版快照

**触发时机：** 生成草稿保存时

**存储位置：** `.agent/{chapter}-draft-ai.md`

**内容：** AI 生成的完整草稿，不压缩不改名

### 2. Diff 对比

**触发时机：** 作家确认归档前

**对比命令：** `diff .agent/{chapter}-draft-ai.md {project}/archives/{chapter}-draft.md`

**输出：** `.agent/{chapter}-draft.diff.md`

### 3. 作家回顾

**触发时机：** 归档前（章完成后一次性回顾）

**Skill 追问方式：**
> "这章你修改了几处。是否记录以下模式？  
> 1. [段1] AI写：... → 你改：...（保留/跳过）  
> 2. [段2] ..."

**作家回答：** "1保留 2跳过" 或 "这段满意" 或直接说"记一下这个"

**记录格式：**

```markdown
## 情绪描写类

- 场景：紧张/恐惧描写
- ❌ AI原文：[心跳加速，感到恐惧]
- ✅ 作家改法：[他站在原地，喉咙像被什么东西堵住了]
- 原因：AI喜欢用抽象情绪词，作家偏好用身体反应暗示情绪

## 对话类

- 场景：人物对话
- ❌ AI原文：[她抬起头，惊讶地说道...]
- ✅ 作家改法：[直接引语，不用动作标签]
- 原因：动作和对话自然交织，不贴情绪标签
```

### 4. 提示词注入

**触发时机：** 每次生成提示词时

**读取顺序：**
1. `{project}/.memory/anti-ai.md`
2. `{project}/.memory/writer-style.md`
3. `references/anti-ai/{genre}/defaults.md`
4. `references/writer-style/{genre}/defaults.md`

**Agent 整合：**
- 语义去重
- 合并冲突（标注 `[作家偏好]` / `[社区defaults]`）
- 提炼为注入规则

**注入位置：** 提示词"写作风格"部分

**注入示例：**
```markdown
## 写作风格

参考作家偏好：
- [作家偏好] 避免抽象情绪词，用身体反应+动作暗示情绪
- [作家偏好] 对话少用情绪标签，动作自然穿插

参考社区defaults：
- [社区defaults] 悬疑类避免过度解释，留白让读者自己体会
```

### 5. 社区贡献

**触发时机：** 作家主动说"贡献这个模式"

**流程：**
1. Skill 读取 `.memory/anti-ai.md` 或 `.memory/writer-style.md`
2. 提取适合社区的条目，重写为 community-ready 格式
3. 生成 `references/anti-ai/{genre}/defaults.md` 或 `references/writer-style/{genre}/defaults.md` 候选文件
4. 引导作家提 PR 或 fork

## 触发时机

| 时机 | 行为 |
|-----|------|
| 归档完成 | Skill 自动 diff，触发回顾追问 |
| 作家主动 | 作家说"记一下这个"，Skill 立即记录上下文 |
| 生成提示词 | 自动读取记忆并注入 |

## 生命周期

| 文件 | 时效 | 管理方 |
|-----|------|------|
| `.agent/*-ai.md` | 临时，本章归档后删除 | Skill |
| `.agent/*-diff.md` | 临时，回顾完成后删除 | Skill |
| `.memory/*.md` | 持久，积累作家偏好 | 作家私有 |
| `references/*/defaults.md` | 持久，社区共享 | Skill+社区 |

## 关键约束

- `.memory/` 追加写入，不覆盖
- `.agent/` 临时文件，章归档后清理
- 作家本地记录优先于 references defaults
- Agent 负责语义去重和冲突合并