---
name: novel-agent
description: 人类与AI协作写小说的工作流系统。Use when 用户想要创建新小说项目、设计世界设定和角色、规划卷章节、生成小说正文。
---

# Novel Agent Skill

人类与AI协作写小说的工作流系统。

## Overview

Novel Agent 是一个小说创作工作流引导者，帮助作者从零开始完成小说的世界设定、角色塑造、情节规划，并通过 AI 生成高质量的章节内容。

核心原则：
- 过程文件全程 YAML 化，归档后为 Markdown
- Agent 与作者逐步讨论确认，每步可追溯
- 步步授权（默认）或全部授权模式

## When to Use

- 用户说"写小说"、"创建小说项目"
- 用户说"讨论世界设定"、"设计角色"
- 用户说"规划章节"、"写第X章"
- 用户说"生成正文"、"继续写"

**When NOT to use:** 用户只是想聊小说内容、不需要系统化工作流。

## Process

### Phase 1: Init - 创建项目

```
输入: create novel [项目名]

步骤:
1. 调用 python scripts/init.py [项目名]
2. 脚本创建目录结构和空壳模板
3. 询问作者 title 和 author
4. 写入 story.yaml
```

### Phase 2: 设定阶段 - 世界设定 & 角色设定

```
输入: 设定阶段开始

世界设定讨论:
1. 用表单问世界类型（玄幻/科幻/悬疑/都市/其他）
2. 用自然语言引导描述地理、政治、文化、历史、规则等
3. 总结确认后写入 settings/world-setting.yaml

角色设定讨论:
1. 用表单列出角色名
2. 对每个角色用自然语言讨论:
   - cognition (认知)
   - worldview (世界观)
   - self_identity (自我定位)
   - values (价值观)
   - abilities (能力)
   - skills (技能)
   - environment (环境)
3. 用表单收集 role (protagonist/antagonist/supporting)
4. 每角色讨论完创建 settings/character-setting/[角色id].yaml
```

### Phase 3: 故事线拆分 + 卷纲 + 章纲

```
输入: 设定阶段完成

流程（以卷1为例）:
1. 讨论卷1卷纲
2. 讨论卷1章1章纲 → 创建 chapters/vol-1-ch-1.yaml
3. 重复直到本卷所有章节
4. 进入下一卷，直到所有卷完成

章纲内容:
- summary: 本章核心情节点
- key_points: 本章要点列表
- characters: 本章涉及的角色列表
- location: 场景地点
- time: 时间背景
```

### Phase 4: 提示词生成

```
输入: 章纲确认 (outline_status: confirmed)

步骤:
1. 读取 story.yaml, volumes/volume-N.yaml, chapters/vol-N-ch-M.yaml
2. 读取 settings/world-setting.yaml
3. 读取相关角色 yaml
4. 读取 settings/writing-style.yaml
5. 组装提示词 yaml
6. 提供3个变体选项供选择
7. 作者不满意则修改
8. 确认后保存到 chapters/prompts/vol-N-ch-M-prompt.yaml
```

### Phase 5: 正文生成

```
输入: 提示词 yaml 已确认

步骤:
1. 调用 subagent，传递提示词 yaml 路径
2. subagent 一次生成完整章节
3. 返回正文给主 Agent 和作者
```

### Phase 6: 归档

```
输入: 作者审阅正文并满意

步骤:
1. 写入 archives/vol-{N}-ch-{M}-{slugified-title}.md
2. 分析正文，推算角色状态变化
3. 更新角色 yaml 的 state_history
4. 更新 chapter 状态为 archived
5. 更新 story.yaml 的 chapters 列表
```

## 提示词 YAML 格式

提示词 yaml 由 Agent 生成，包含完整上下文供 subagent 独立写作：

```yaml
prompt_version: "1.0"
chapter_ref:
  volume: 1
  chapter: 1
  title: "第1章标题"

role: |
  你是全球闻名的小说作家...

core_principles:
  global_rules:
    - "客观对待，不带道德化..."
    - "保持世界观逻辑推进..."
  natural_expression: [...]
  description_vs_depiction: [...]
  character_building: [...]

possible_mistakes: [...]

depiction_techniques: [...]

context:
  world_setting: {...}
  characters: [...]
  plot: {...}
  scene: {...}

content: |
  [章纲内容]
```

## 授权模式

- **步步授权（默认）**: 每步需作者确认
- **全部授权**: Agent 全权决定

作者可随时说"你全权决定"或"每步都要我确认"切换模式。

## Common Rationalizations

- "作者没回应我就继续往下走" → 必须等待确认
- "章纲差不多就行，不用那么详细" → 细节决定质量
- "角色设定差不多了，直接开始写" → 基础不牢地动山摇
- "提示词生成完不用给作者选了" → 作者选择权是核心流程

## Red Flags

- 跳过 Phase 2 直接进入 Phase 3
- 不更新 story.yaml 就往下走
- subagent 生成正文时上下文不完整
- 正文写完不归档就直接结束
- 不更新角色 state_history

## Verification

检查清单：
- [ ] story.yaml 存在且包含正确的项目信息
- [ ] 每个设定阶段都有作者确认记录
- [ ] 章纲包含所有必需字段 (summary, key_points, characters, location, time)
- [ ] 提示词 yaml 包含完整上下文
- [ ] 归档后的 markdown 命名正确 (vol-{N}-ch-{M}-{title}.md)
- [ ] 角色 state_history 在归档时更新

## Subagent 调用方式

```
Agent 调用 subagent 写正文：
- 传递: 提示词 yaml 路径
- subagent 读取提示词 yaml
- subagent 生成正文（一次生成完整章节）
- 返回正文给主 Agent
```
