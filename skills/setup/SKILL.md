---
name: novel-setup
description: 小说项目初始化与设定。Phase 1+2。当项目尚未创建、world-setting.yaml 为空、或用户说"创建项目""讨论设定""设计角色""世界观""写作风格""题材""导入小说"时必须使用。即使只说"帮我开始写小说"也要先加载本技能完成设定。
---

# Novel Setup — 项目初始化与设定

## Overview

引导作者完成项目创建、世界观搭建、角色塑造、写作风格确认。Phase 2 末尾生成全局提示词，全本复用。

**When NOT to use:** 项目已创建且设定完整（world-setting、角色、writing-style 均非模板）、只是想查看设定内容。

**Announce at start:** "我来引导你完成小说设定。先确认项目基本信息。"

## HARD-GATE

```
所有 YAML 文件必须经作者讨论确认后才能写入。
严禁看到模板格式就自行填充。
```

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
6. **STOP：** 作者决定——"缺的后面再说"→ Phase 4 / "先补几项"→ 引导补充 / "缺太多"→ Phase 2

**从导入模式进入 Phase 2 时：** Agent 先检查 `settings/writing-style.yaml` 是否为模板默认内容。若是默认模板 + 反向提取到的风格特征 → 报告差异，让作者选择："保留默认模板 / 用反向提取到的风格覆盖 / 混合调整"。确认后再进入 Phase 2。

## Best Practices

**选题引导：** 不只是问作者"什么题材"——帮他从社会热点、身边事件中提取故事灵感。小人物牵出大事件比大场面开局更有代入感。例：一个外卖员无意间拍到的视频→牵扯出旧城改造的腐败案。

**角色身份塑造：** 主角不一定要超人开局。"天崩开局"（巨债、绝症、灭门）比完美开局更好写，也更容易让读者共情。例：主角剩三个月寿命→破罐破摔疯狂花钱→意外中了彩票→现在不想死了。

**角色目标设计：** 目标是活的，会随着剧情发展改变。好的目标变化本身就是故事弧光。例：主角从"痛快花钱不留遗憾"→"发横财后想活着"→目标变了，冲突就来了。

**画面感练习：** 引导作者描述场景时问"你看到的画面是什么"，然后逐层展开——视觉（硝烟/血/旗帜）、听觉（耳鸣/厮杀声）、嗅觉（血腥味）、触觉（伤口的剧痛）、内心（绝望/不甘）。

## Phase 2: 设定阶段

顺序不可跳过。讨论角色身份、目标、画面感和写作风格时，参考 `best-practices.md` 中的案例引导作者。

### 世界观

1. AskUserQuestion 问世界类型
2. 逐领域引导描述：geography → politics → culture → history → rules → physics → biology → sociology
3. 每领域即时确认，全部确认后写入 world-setting.yaml

### 角色设定

1. AskUserQuestion 收集角色名列表
2. 逐角色讨论：cognition、worldview、self_identity、values、abilities、skills、environment
3. story_role：protagonist / antagonist / supporting / minor
4. 每角色讨论完创建 `settings/character-setting/[拼音id].yaml`

### 写作风格确认

1. 告知作者：writing-style.yaml 已预填"低 AI 味优化版"默认设定（自然松弛、句式强制、禁止堆技法）
2. AskUserQuestion："使用默认 / 调整 / 用自己的风格"

### 题材配置

1. 确定题材类型
2. 讨论爽点类型、节奏红线、反套路规则
3. 写入 genre 字段

### 钩子初始化

1. 引导浏览 hooks.yaml 了解生命周期
2. 有伏笔想法写入，无则留空后续填充

### author-intent.md

引导填写核心主题、终局方向、写作信条。至少填核心主题和写作信条。**STOP：作者确认。**

### 生成全局提示词

1. 读取 writing-style.yaml 全部字段，按 prose 组装 `prompts/global-prompt.md`
2. 内容：角色定位 + 写作原则与禁忌（🔴🟡🟢三层分离）+ 欲望引擎与代入感 + 题材规则
3. 展示确认。此文件永不再改。
4. **STOP：作者确认后告知"设定完成。下一步可以规划章节了。说出'规划章节'开始。"**

## 下一步

完成后引导作者进入 Phase 3。当作者说"规划章节"时，母技能路由到 `novel-outline`。
