---
name: novel-setup
description: 小说项目初始化与设定。Phase 1+2。当项目尚未创建、world-setting.yaml 为空、或用户说"创建项目""讨论设定""设计角色""世界观""写作风格""题材""导入小说"时必须使用。即使只说"帮我开始写小说"也要先加载本技能完成设定。
---

# Novel Setup — 项目初始化与设定

> 摘要：init.py 创建骨架 → 逐项讨论设定 → 写入 YAML → 生成 global-prompt.md。作者每项确认。

## Overview

引导作者完成项目创建、世界观搭建、角色塑造、写作风格确认。Phase 2 末尾生成全局提示词，全本复用。

**When NOT to use:** 项目已创建且设定完整（world-setting、角色、writing-style 均非模板）、只是想查看设定内容。

**Announce at start:** "我来引导你完成小说设定。先确认项目基本信息。"

## 执行前提

执行任何写入操作前，read_file 查看目标 YAML 是否已是模板默认值。若不是 → 作者已确认过，追加不覆盖。所有写入后展示变更摘要，等作者确认才保存。

## Phase 1: 创建项目

### 情况 A：新建小说

1. 执行 `python ~/.claude/skills/novel/scripts/init.py [项目名] [--author 作者名]`
2. 询问作者 title 和 author（若未通过 --author 传入）
3. 将 title、author、created_at 写入 story.yaml

### 情况 B：导入已有小说

1. 执行 init.py 创建骨架
2. 请作者提供已有小说文件（.txt / .md）
3. 执行 `python ~/.claude/skills/novel/scripts/import.py [项目路径] [小说文件]`
4. Agent 逐章阅读，反向提取 → world-setting、角色、写作风格、钩子
5. 输出导入完整性报告（✅已提取 / ⚠️已推测 / ❌未找到）
6. **STOP：** 作者决定——"缺的后面再说"→ 继续写正文（chapter-loop）/ "先补几项"→ 引导补充 / "缺太多"→ Phase 2

**从导入模式进入 Phase 2 时：** Agent 先检查 `settings/writing-style.yaml` 是否为模板默认内容。若是默认模板 + 反向提取到的风格特征 → 报告差异，让作者选择："保留默认模板 / 用反向提取到的风格覆盖 / 混合调整"。确认后再进入 Phase 2。

## Phase 2: 设定阶段

顺序不可跳过。每步讨论时参考 `best-practices.md` 中的案例引导作者。

### 世界观

1. AskUserQuestion 问世界类型
2. 按 world-setting.yaml 模板的字段（geography → politics → culture → history → rules → physics → biology → sociology）逐项引导，每项即时确认
3. 全部确认后写入 world-setting.yaml
4. **诊断：** "这个设定能通过角色经历的场景呈现吗？"

### 角色设定

1. AskUserQuestion 收集角色名列表
2. 按 character.yaml 模板字段（cognition → worldview → self_identity → values → abilities → skills → environment）逐角色讨论
3. 填写 story_role（protagonist / antagonist / supporting / minor）
4. 每角色讨论完创建 `settings/character-setting/[拼音id].yaml`
5. **逐角色诊断：** "TA 生气时怎么表现？和其他角色有什么不同？" "TA 有什么缺点？" "配角除了服务剧情，自己有什么目的？"

### 写作风格确认

1. 告知作者：writing-style.yaml 已预填"低 AI 味优化版"默认设定（自然松弛、句式强制、禁止堆技法、禁用诗词腔）
2. AskUserQuestion："使用默认 / 调整 / 用自己的风格"
3. **诊断：** "你最喜欢的三本小说/三部电影是什么？它们哪里最吸引你？"（参考 best-practices.md「写作风格」）

### 类型档案选择

写作风格确认后，引导作者选择预置类型档案。类型档案是预制的"类型知识库"——包含该类型的文风/氛围/专属要素/禁忌，选类型即注入，无需每次从零讨论。

1. 读取 `~/.claude/skills/awesome-novel/genre-corpus/index.yaml` 的 `genres` 列表，提取 `id`、`label`、`description`
2. AskUserQuestion 列出可用类型档案（扁平列出所有 24 种，作者看不到继承关系）+ "暂不选择（手动配置题材）"选项
3. 作者选择后，展示档案摘要：
   - **文风文笔**：`style_blueprint.voice`（摘要，前 2 句）
   - **核心氛围**：`style_blueprint.atmosphere`（摘要，前 2 句）
   - **专属要素**：`style_blueprint.genre_elements` 列表
   - **叙事视角**：`style_blueprint.pov_description`
   - **类型禁忌**：`genre_taboos` 列表
4. **STOP：作者确认或提出调整。** 作者可以：
   - "确认" → 直接应用
   - "用这个但去掉XX禁忌" → 调整后应用
   - "用这个但氛围我想改成XX" → 微调后应用
5. 应用类型档案（合并算法见 `skills/prompt/SKILL.md` Step 2，本处只写结果）：
   - 写入 `genre_profile: "{id}"` 到 writing-style.yaml
   - 合并 genre_config（satisfaction_types / chapter_types / pacing_rules / anti_cliches）到 writing-style.yaml 的 genre 字段
   - 追加 genre_fatigue_words 到 anti-ai.yaml 对应分类
   - style_blueprint、genre_taboos、prompt_segment 保留在 corpus 文件中，chapter-loop Step 3 时读取

选择"暂不选择"则跳过此步，后续题材配置从零讨论。

### 题材配置

1. 若已选择类型档案 → 展示已合并的 genre_config，问作者"需要调整吗？"（快速确认，无需从零讨论）
2. 若未选择类型档案 → 确定题材类型、讨论爽点类型、节奏红线、反套路规则
3. 写入/更新 genre 字段
4. **诊断（参考 best-practices.md「题材诊断」）：** "书名和标签写的是什么题材？正文第一章读者能立刻感受到这个题材的核心味道吗？"

### 钩子初始化

1. 引导浏览 hooks.yaml 了解生命周期
2. 有伏笔想法写入，无则留空后续填充


### 生成全局提示词（可选——作者参考文档）

1. 读取 writing-style.yaml 全部字段，组装 `prompts/global-prompt.md`
2. 用大白话写，不用 emoji 分类（🔴🟡🟢），不编号。内容是写作方法论汇总——角色定位、核心原则、禁止事项、题材规则、技法参考
3. **注意：** 此文件是供作者审阅的参考文档。chapter-loop Step 3 的章提示词直接从 writing-style.yaml 实时提取约束并用自然语言重述，不从 global-prompt.md 复制粘贴
4. 展示确认。
5. **STOP：作者确认后告知"设定完成。下一步可以规划章节了。说出'规划章节'开始。"**

## 下一步

完成后引导作者进入 Phase 2（novel-volume）。当作者说"规划章节"时，主 Agent Read `skills/outline/SKILL.md` 进入 Phase 2。
