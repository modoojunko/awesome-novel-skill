---
name: novel-setup
description: 小说项目初始化与设定。当项目尚未创建、world-setting.md 为空、或用户说"创建项目""讨论设定""设计角色""世界观""写作风格""题材""导入小说"时必须使用。即使只说"帮我开始写小说"也要先加载本技能完成设定。
---

# Novel Setup — 项目初始化与设定

> 摘要：init.py 创建骨架 → 逐项讨论设定 → 写入文件。作者每项确认。

## Overview

引导作者完成项目创建、题材选择、世界观搭建、角色塑造、写作风格确认。

**When NOT to use:** 项目已创建且设定完整（world-setting、角色、writing-style 均非模板）、只是想查看设定内容。

**Announce at start:** "我来引导你完成小说设定。先确认项目基本信息。"

## 工具契约

| 工具 | 用途 | 限制 |
|------|------|------|
| Bash | 执行 `init.py` 创建项目骨架 | 不安装新包，不改系统配置 |
| Read | 读 init.py（获知骨架结构）、references/ 各指南文件、genre-example 类型档案 | — |
| Write/Edit | 写 story.md、settings/ 下所有设定文件、character-setting/*.md | 追加不覆盖（角色文件已有时不删减） |
| WebSearch | 作者要求导入/分析参考作品时查风格 | 仅在风格讨论阶段使用 |

## 错误恢复

| 失败场景 | 恢复策略 |
|---------|---------|
| `init.py` 不可用或报错 | 手动创建目录结构 + 复制 scripts/templates/*.template 到对应路径去 .template |
| 作者未选择类型档案 | 跳过类型档案步，后续题材配置从零聊 5 个字段 |
| 角色文件已存在（追加场景） | 读已有文件，只追加不覆盖。认知 6 层已有则不重复讨论 |
| 作者跳过某个设定 | 跳过写入，对应字段留空，在 story.md 中标记"待补充" |

## 执行前提

执行任何写入操作前，read_file 查看目标文件是否已是模板默认值。若不是 → 作者已确认过，追加不覆盖。所有写入后展示变更摘要，等作者确认才保存。

## 创建项目

1. 执行 `python $NOVEL_SKILL_HOME/scripts/init.py [项目名] [--author 作者名]`
2. 询问作者 title 和 author（若未通过 --author 传入）
3. 将 title、author、created_at 写入 story.md

## 设定阶段

顺序不可跳过。每步先读对应的指南文件，按指南的引导流程执行。

### 先选题材（定类型，为后续提供上下文）

Read `references/genre-style.md`「先选题材」部分，用对话引导法从作者描述中提取信号确定类型。**定了题材再聊世界观和角色**——题材不同，世界观该聊的层级和角色的常见配置都不同。

确认后记下类型 id，不写文件（后续题材配置步统一写入）。

### 写作风格确认

1. 告知作者：writing-style.md 已预填"低 AI 味优化版"默认设定（自然松弛、句式强制、禁止堆技法、禁用诗词腔）
2. AskUserQuestion："使用默认 / 调整 / 用自己的风格"
3. **诊断：** "你最喜欢的三本小说/三部电影是什么？它们哪里最吸引你？"

### 类型档案选择（可选）

写作风格确认后，询问是否使用预置类型档案。类型档案是预制的"类型知识库"——包含该类型的文风/氛围/专属要素/禁忌，选类型即注入，无需从零聊题材配置。

1. 读取 `$NOVEL_SKILL_HOME/references/genre-example/index.md` 的 `genres` 列表，提取 `id`、`label`、`description`
2. AskUserQuestion 列出可用类型档案（扁平列出所有 24 种）+ "暂不选择，手动配置"选项
3. 作者选择后，展示档案摘要：文风文笔、核心氛围、专属要素、叙事视角、类型禁忌
4. **STOP：作者确认或提出调整**
5. 确认后应用类型档案：
   - 写入 `genre_profile: "{id}"` 到 writing-style.md
   - 合并 genre_config 到 writing-style.md 的 genre 字段
   - 追加 genre_fatigue_words 到 anti-ai.md
   - style_blueprint、genre_taboos、prompt_segment 保留在 corpus 文件中

选择"暂不选择"则跳过此步，后续题材配置从零讨论 5 个字段。

### 题材配置（5 字段）

Read `references/genre-style.md`，按 5 个字段逐项填写。写入 `settings/genre-setting.md`。

- **已选择类型档案** → 展示已合并的 genre_config，问作者"需要调整吗？"（快速确认，无需从零讨论）
- **未选择类型档案** → 按 genre-style.md 的 5 个字段逐项聊：满足类型 / 节奏规则 / 避免套路 / 类型禁忌（选定类型已在"先选题材"步确定）
- 写入 `settings/genre-setting.md`（独立文件，非 writing-style.md 字段）
- **诊断：** "书名和标签写的是什么题材？正文第一章读者能立刻感受到这个题材的核心味道吗？"

### 世界观（3 项）

Read `references/world-setup-style.md`，按三项逐项聊，每项过自检再进下一项：

1. **地理** — 主角在哪 → 怎么去 → 路上什么样（从场景出发，不画地图）
2. **政治** — 谁说了算 → 谁限制他 → 不服会怎样（至少 2 个势力）
3. **规则** — 先问不能做什么，再问能做什么（世界级/社会级/个人级三层，每规则三要素：能/不能/代价）

写入 `settings/world-setting.md`，用 `## 地理` / `## 政治` / `## 规则` 三级标题。完成后走指南中的三步总检。

### 角色设定

Read `references/character-setting-style.md`，按以下流程执行：

1. 收集角色名列表，确定故事角色类型（protagonist / antagonist / supporting）
2. 填写**基本信息**（外貌 / 背景 / 语言特征）
3. 按**认知 6 层模型**（世界观 → 自我定位 → 价值观 → 能力 → 技能 → 环境）逐角色讨论
4. 每角色创建 `settings/character-setting/[拼音id].md`
5. 走**两步总检**（格式检查 + 可用性检查）
6. 可选**角色活检**（场景扮演测试：Agent 根据角色设定生成 3 个测试场景，以角色身份回答，作者判断"像不像"）

## 完成报告

所有设定写入后，展示给作者：

```
设定完成。
──────────────────────────────
✅ 已写入：
  - story.md（标题/作者/创建时间）
  - settings/writing-style.md（风格配置）
  - settings/genre-setting.md（题材 {id}）
  - settings/world-setting.md（地理/政治/规则）
  - settings/character-setting/（N 个角色）
📌 待补充字段：
  - world-setting.md → 个人级规则（如需）
  - character-setting/*.md → 语言特征、情绪弧线（写作中追加）
──────────────────────────────
设定阶段完成。下一步：规划故事主线 + 卷纲。
欢迎随时回来修改设定。
```

## 下一步

1. 更新 `.agent/status.md`：将 `current_phase` 改为 `volume`
2. 引导作者进入 `skills/outline/SKILL.md`。当作者说"规划章节"时，主 Agent Read `skills/outline/SKILL.md` 进入主线拆纲+卷纲。
