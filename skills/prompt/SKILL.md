---
name: novel-prompt
description: 章提示词生成与视角转换。Phase 4。当章纲已确认、需要为 subagent 准备完整写作指令时必须使用——视角转换 + 三层提示词合并（全局+卷+章专属）。触发："生成提示词""视角转换""组装章提示词""准备写作材料"。写正文前必须经此步骤，不可跳过直接写。
---

# Novel Prompt — 章提示词生成

## Overview

视角转换 + 三层合并：全局提示词全文 + 卷提示词全文 + 本章专属 prose → 一个格式文件。subagent 只读这一个文件。

**When NOT to use:** 章纲不完整（memo 或 emotional_design 缺失）、本章提示词已生成且未修改章纲、章状态尚未到 outline。

**Announce at start:** "我来生成本章提示词。先做视角转换。"

## HARD-GATE

```
视角转换必须先单独确认，确认后才能组装章提示词。严禁合并确认。
章提示词 = 全局全文 + 卷全文 + 本章专属。subagent 只读这一个文件。
```

## 进入门禁

| 检查项 | 操作 |
|--------|------|
| `prompts/global-prompt.md` 是否存在？ | 不存在 → 生成（从 writing-style.yaml），作者确认 |
| `prompts/volume-{N}-prompt.md` 是否存在？ | 不存在 → 生成（从 volume.yaml + archives/），作者确认 |
| 模板版本检查 | 读取 `~/.claude/skills/novel/scripts/templates/writing-style.yaml.template` 头部 `# version: N`，对比项目 `settings/writing-style.yaml` 头部版本号。模板版本更高 → 向作者报告"写作风格模板有更新"，列出新增的 global_rules 和 possible_mistakes 条目，问作者"合并新规则 / 暂不合并"。合并后自动重新生成 `prompts/global-prompt.md` |
| 章纲完整性 | memo（7段）+ emotional_design 全部有值？任一为空 → **STOP**，退回 `novel-outline` |
| author-intent.md 一致性 | 本章与核心主题一致 / 存在偏离？偏离 → **STOP** |
| current-focus.md 一致性 | 本章在优先级范围内 / 偏离？偏离 → **STOP** |

## 第一轮：视角转换

1. 读取 chapter.yaml 的 outline 字段
2. **确认叙事视角**：读 narrative_pov。空 → 询问作者确认（第三人称有限/第一人称/全知）
3. 按视角转换规则将上帝视角章纲转为沉浸式写作指引
4. **STOP：展示（含叙事视角），等确认。**

### 视角转换规则

一句话：**把"发生了什么事"重写为"事情发生时，在场的人感受到了什么"。**

- 禁止"本章讲述了""主角经历了"等上帝视角概述语
- 指引是地图，不是已经走完的路。只描述场景基调、关键情节点、情感走向，把叙事节奏和语言组织留给 subagent
- **字数上限**：不超过章纲 outline 字数的 2-3 倍
- **禁止写具体对话**：只描述对话的目的和走向
- **禁止写动作细节**：只描述动作的结果和意义
- 写完自检——如果 subagent 照着做文字整理就能交稿 → 粒度太细了

### 钩子兑现锚定

若 payoff_plan 有 resolve 或 partial_advance 的钩子 → 必须将 seed_text 嵌入写作指引："> 读者在第 X 章看到过：'[原文引用]'——本章需要接着这个画面来写兑现。"

### 爽感循环感知

读取 cycle_position，注入对应策略：
- **压制章**：写具体的"债"，不写"主角很惨"；压制比上一轮更过分；章尾暗示"快了"
- **释放章**：对应压制章的每一笔债怎么打回去；反派表情 不在乎→慌→崩溃；旁观者反应；余波
- **余波章**：释放后世界变了什么；埋新压制种子

## 第二轮：三层合并

1. 读取 `prompts/global-prompt.md` 全文——原样，第一部分
2. 读取 `prompts/volume-{N}-prompt.md` 全文——原样，第二部分
3. 以 chapter.yaml 字段为过滤键，精准读取源文件生成第三部分：

**故事背景（一段）：**
- world-setting 全局规则（每章必带，不过滤）：力量/法术体系、科技水平、特殊世界规则（时间循环/系统/鬼怪机制）、社会结构、当前世界大势、世界基调。这些是世界的底层规则——无论主角在哪都在起作用
- world-setting 场景片段：只取与 location + time 相关的局部设定
- 角色快照：只读 outline.characters 列出的角色（姓名、定位、当前状态、关系、state_history、worldview/values）。禁止只写角色名
- **回忆/闪回检测**：检查 outline.summary 和 memo 是否涉及回忆、往事、过去场景。若是 → 读取相关角色的**完整 state_history**（不只是最近 1-2 条）+ 从 archives/ 提取涉及该角色过往关键场景的原文片段（每段 100-150 字）。确保 subagent 写的回忆与已确认的正文一致，不凭空编造
- 前章锚定：上一章正文结尾最后 150-200 字原文引用。让 subagent 知道读者刚刚看到什么画面，保证章节衔接无缝
- 活跃钩子速览：所有 status != resolved 的钩子列表（只列标题+当前状态，不展开正文）。防止正文意外踩坑或遗漏

**写作指引（一段）：**
- 视角转换结果 + memo + emotional_design
- hooks.yaml：只读 payoff_plan 涉及的钩子

**写作执行清单（一段，PRE_WRITE_CHECK prose）：**
- current_task、reader_expectation、payoff_plan、required_changes、micro_payoffs、cycle_position、prohibitions

**写作要求（一段）：**
- 字数下限、节奏方向、爽感循环策略、微兑现要求

4. 合并三部分，对写作指引生成 3 个变体（主角视角/场景氛围/冲突切入），全局和卷部分相同
5. **STOP：展示章提示词（含变体选择），等确认。**
6. 确认后保存 `prompts/vol-{N}-ch-{M}-prompt.md`，status → draft

## 下一步

完成后引导进入 Phase 5。当作者说"写正文"时，母技能路由到 `novel-write`。
