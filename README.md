<p align="center">
  <strong>Novel Agent</strong><br>
  <em>和 AI 一起写小说 —— 无需订阅，DeepSeek V4 原生支持</em>
</p>

<p align="center">
  <a href="README-en.md"><img src="https://img.shields.io/badge/English-README-blue?style=flat-square" alt="English README"></a>
  <a href="https://github.com/hust-open-atom-club/DeepSeek-TUI"><img src="https://img.shields.io/badge/DeepSeek%20V4-%E2%9C%93%20%E6%94%AF%E6%8C%81-4FC08D?style=flat-square" alt="DeepSeek V4 TUI"></a>
  <a href="https://docs.anthropic.com/en/docs/claude-code/overview"><img src="https://img.shields.io/badge/Claude%20Code-%E2%9C%93%20%E6%94%AF%E6%8C%81-6B46C1?style=flat-square" alt="Claude Code"></a>
  <a href="https://github.com/hermes/hermes"><img src="https://img.shields.io/badge/Hermes-%E2%9C%93%20%E6%94%AF%E6%8C%81-FF6B6B?style=flat-square" alt="Hermes"></a>
  <a href="https://github.com/openclaw/openclaw"><img src="https://img.shields.io/badge/OpenClaw-%E2%9C%93%20%E6%94%AF%E6%8C%81-FFA94D?style=flat-square" alt="OpenClaw"></a>
  <br>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-GPL%203.0-blue?style=flat-square" alt="GPL 3.0"></a>
</p>

> **个人使用免费** — 本 Skill 对个人用户完全免费。<br>
> **商业使用** — 请联系作者获取授权。

让 AI 成为你的小说创作搭档,从世界观搭建到角色塑造，从章节规划到正文写作，一步步陪你完成整部小说。

## 你需要什么

- 安装了以下任一工具的电脑：[DeepSeek TUI（DeepSeek V4）](https://github.com/hust-open-atom-club/DeepSeek-TUI)、[Claude Code](https://docs.anthropic.com/zh-CN/docs/claude-code/overview)、[Hermes](https://github.com/hermes/hermes) 或 [OpenClaw](https://github.com/openclaw/openclaw)
- 大概 1 分钟完成安装

> **提示**：DeepSeek V4 通过 DeepSeek TUI 完全免费使用，无需 API 费用。

## 安装

根据你用的工具，复制对应那行命令，在终端里粘贴执行：

### DeepSeek V4（DeepSeek TUI）

```bash
git clone https://github.com/modoojunko/awesome-novel-skill.git && cd awesome-novel-skill && ./install.sh deepseek-tui
```

### Claude Code

```bash
git clone https://github.com/modoojunko/awesome-novel-skill.git && cd awesome-novel-skill && ./install.sh claude-code
```

### Hermes

```bash
git clone https://github.com/modoojunko/awesome-novel-skill.git && cd awesome-novel-skill && ./install.sh hermes
```

### OpenClaw

```bash
git clone https://github.com/modoojunko/awesome-novel-skill.git && cd awesome-novel-skill && ./install.sh openclaw
```

如果上面那行不行，手动来（也是复制粘贴，以 DeepSeek V4 为例）：

```bash
git clone https://github.com/modoojunko/awesome-novel-skill.git
cd awesome-novel-skill
mkdir -p ~/.deepseek/skills/awesome-novel
cp -r agents ~/.deepseek/skills/awesome-novel/
cp -r templates ~/.deepseek/skills/awesome-novel/
cp -r knowledge ~/.deepseek/skills/awesome-novel/
cp -r memory ~/.deepseek/skills/awesome-novel/
cp -r tools ~/.deepseek/skills/awesome-novel/
cp SKILL.md CLAUDE.md ~/.deepseek/skills/awesome-novel/
```

> Claude Code 用户把路径换成 `~/.claude/skills/awesome-novel`，Hermes 用户换成 `~/.hermes/skills/awesome-novel`，OpenClaw 用户换成 `~/.openclaw/skills/awesome-novel`。

看到 "安装完成" 就可以了。

> **看到这个项目觉得有用？** 顺手点个 Star，这样它会出现在你的 GitHub 首页，让更多人发现。
> {: .prompt-info }

## 开始写小说

安装后，打开终端，在**你想放小说项目的目录**下启动你的 AI 工具，然后说一句：

> **帮我写本小说**

系统会自动加载写作流程。后续再进入该项目时，说 `@novel-agent` 或 **"帮我继续写"** 就能从中断处恢复。

Agent 会引导你完成后续步骤。系统由 7 个 AI Agent 协作驱动，自动检测进度、调度任务，你只需确认方向和审阅内容。

### 一次性设定

第一次写小说时，Agent 会和你聊这几个方面。**不用一次性想好全部**，想不到的跳过，后面随时补：

1. **题材选择** — 仙侠、都市、悬疑、历史……说你脑子里想的那个就行。Agent 会按题材类型自动配置写作风格和节奏模板。也可以直接从 24 套预置题材画像里选一个，省去手动调风格的步骤
2. **世界观** — 故事发生在什么世界？有什么特殊规则？（比如"修仙世界，灵根决定天赋"）
3. **主要角色** — 主角是谁？TA 是什么样的人？Agent 会逐个角色和你讨论性格、能力、成长经历
4. **写作风格** — 偏好更偏描写还是更偏对话、更古风还是更现代？也可以导入你喜欢的小说来提取文风

### 项目结构

设定聊完后，Agent 会在当前目录下创建你的小说项目，结构如下：

```
{你的小说文件夹}/
├── story.md              # 项目总索引（元信息/主线/卷规划）
├── settings/             # 设定文件
│   ├── world-setting.md  # 世界观
│   ├── writing-style.md  # 写作风格
│   ├── genre-setting.md  # 题材设定
│   ├── timeline.md       # 时间线
│   └── character-setting/ # 角色档案
│       └── <id>.md       # 每个角色一个文件
├── volumes/              # 卷纲
├── chapters/             # 章纲
├── prompts/              # 提示词
├── archives/             # 正文（定稿）
├── .agent/               # Agent 进度数据
└── .claude/              # Agent 定义 + 知识库 + 写作记忆
    ├── agents/           # Agent 定义
    ├── knowledge/        # 反 AI 规则、文风偏好、永久记忆
    └── memory/           # 写作动态记忆（各环节作者反馈）
```

这些全是纯文本 Markdown 文件，你可以直接用编辑器打开看或手动改。

### 规划故事骨架

设定聊完后，Agent 帮你规划整体故事结构：

1. **主线拆纲** — 一句话说清全书核心冲突，然后从结局倒推，拆成几个大阶段
2. **分卷规划** — 每个阶段就是一卷，每卷大概写什么、到什么位置
3. **定第一卷章节** — 第一卷分几章，每章的核心内容

> **不知道结局？** 告诉 Agent"我只知道开头"，它照样帮你规划第一卷。

### 逐章写作循环（Agent 协作）

多 Agent 协作自动推进，你只需审阅和决策：

| 步骤 | 负责 Agent | 做什么 |
|------|-----------|--------|
| **① 章纲** | chapter-planner | 分析前文和设定，给出分镜、情绪设计和钩子计划。你看完后说"可以"或"改一下" |
| **② 提示词** | prompt-crafter | 根据章纲、反 AI 规则和文风偏好，组装 9 层纯净提示词 |
| **③ 写正文** | writer | 按提示词写完整一章，自动净化 AI 腔 |
| **④ 审阅** | reader（可选） | 10 维 60+ 细项深度评审，对照章纲/设定/前文逐条诊断 |
| **⑤ 归档** | updater | 你确认后归档定稿，自动更新角色状态、追加情绪弧线、合并文风偏好、检测钩子健康和卷边界 |

第一章写完后，Agent 会问"下一章继续吗？"

### 自动做的事（Agent 维护）

- **去 AI 味**（prompt-crafter + writer）：提示词组装时注入反 AI 规则，正文生成时自动规避疲劳词、句式模板、元叙事
- **动态记忆**（多 agent + updater）：各 agent 在对话中实时记录你的写作偏好和反馈（正反案例），归档时 updater 兜底清理、去重压缩。高频使用的规则自动晋升为永久记忆（`.claude/knowledge/permanent-memory.md`），越写越懂你
- **记伏笔**（updater）：归档时自动扫描未兑现/新埋的钩子，检测陈旧度和集中收束风险
- **管角色状态**（updater）：每章归档后自动追加角色状态历史、情绪弧线和人际关系变化。下一章写作时 Agent 知道最新状态
- **节奏检查**（updater）：连续高压超过 3 章或连续平淡超过 2 章，提醒你调整
- **卷边界检测**（updater）：整卷完成后自动输出报告，询问下一卷方向

### 常用指令

| 你说 | AI 做什么 |
|------|-----------|
| "帮我写本小说" | 首次加载技能 + 创建项目 + 设定讨论 |
| "@novel-agent" 或 "帮我继续写" | 进入 / 恢复写作循环 |
| "写下一章" | 开始写最新一章 |
| "改一下第 X 段" | 修改指定段落 |
| "这章写完了" 或 "归档" | 确认本章完成 |
| "看看进度" | 查看当前写了多少 |
| "导入这本小说" | 导入已有草稿继续写 |
| "迁移项目" | 从旧版自动迁移到 4.0 格式 |
| "solo" 或 "你全权写" | 进入全自动模式，不打断你确认 |

## 三种协作模式

| 模式 | 触发词 | 行为 |
|------|--------|------|
| **步步确认**（默认） | — | 每做一步都等你点头才继续 |
| **全部授权** | "你全权决定" | 流程节点还在，Agent 代按确认，不经你手 |
| **SOLO 模式** | "solo" / "单机" | 流程简化，无 STOP 点，Agent 一人完成全部创作和写作。适合让 AI 放飞写 |

随时可以切换，跟 Agent 说一声就行。

## 更高阶的玩法

### 预置题材画像

不想从头设定写作风格？Agent 在一次性设定阶段就会问你用不用预置风格。项目内置 24 套题材档案，每套包含角色人设倾向、叙事语气和章节提示词模板。涵盖仙侠、都市、悬疑、历史、科幻末世、西方奇幻等主流类型。

### 从喜欢的小说里学文风

有没有特别喜欢的小说，想让 AI 照着那个风格写？

1. 把参考小说文件放进项目目录
2. 跟 Agent 说"分析一下这本小说的文风"
3. Agent 会跑统计分析（句子长短、对话占比、描写密度），再定性提取风格特征，输出一份风格档案给你确认
4. 确认后自动合并到写作配置里，后续所有章节按这个风格写

## 常见问题

**Q: 我不会编程，能装吗？**

能。上面那几行命令复制粘贴到终端，回车就行。唯一的前提是你的电脑上已经装好了 DeepSeek TUI、Claude Code、Hermes 或 OpenClaw。

**Q: 需要订阅 Claude 才能用吗？**

完全不需要。用 DeepSeek V4（DeepSeek TUI）即可免费使用全部功能，无需任何订阅或 API 费用。

**Q: 我升级了技能，之前写的小说项目怎么迁移到新格式？**

升级后首次在当前项目目录启动时，Agent 会自动检测旧版格式，引导你完成迁移。核心逻辑：旧文件整体挪到 `old/` 目录保留备份，在原地初始化新项目骨架，再逐字段将旧版设定转换到新版格式。已归档的正文直接拷贝，正在写的不迁移。确认迁移无误后可手动删除 `old/` 目录。

**Q: 写到一半可以改设定吗？**

可以。随时跟 Agent 说"改一下世界观里的 XXX"或"这个角色的性格我想调整"，它会帮你更新。

**Q: 生成的文字有 AI 味怎么办？**

默认配置就是"低 AI 味"——禁止了常见机器腔句式、写完后自动检测。动态记忆系统会记录你如何修改 AI 原文，提炼为你的专属规则，后续自动规避。

**Q: 可以用自己的写作风格吗？**

可以。项目创建后有专门的写作风格文件，你可以把自己的偏好写进去，后面所有章节都会按这个风格来。

## Star History

<a href="https://star-history.com/#modoojunko/awesome-novel-skill">
  <img src="https://api.star-history.com/svg?repos=modoojunko/awesome-novel-skill&type=date" alt="Star History">
</a>

## 致谢

感谢 [@hust-open-atom-club](https://github.com/hust-open-atom-club) 的 [DeepSeek TUI](https://github.com/hust-open-atom-club/DeepSeek-TUI) 项目为 DeepSeek V4 用户提供免费、流畅的终端体验，让本 Skill 对个人用户完全免费可用。

本项目部分设计受到 [InkOS](https://github.com/Narcooo/inkos) 的启发——包括 AI 味检测体系、伏笔/钩子追踪、题材配置和分层技法模型。感谢 [@Narcooo](https://github.com/Narcooo) 的优秀工作。

## 贡献

欢迎参与贡献！详情请查看 [CONTRIBUTING.md](./CONTRIBUTING.md)。

| 方式 | 说明 |
|------|------|
| [Bug 反馈](https://github.com/modoojunko/awesome-novel-skill/issues/new) | 报告功能异常、安装问题 |
| [功能建议](https://github.com/modoojunko/awesome-novel-skill/issues/new) | 提出新功能或改进想法 |
| [素材扩充](https://github.com/modoojunko/awesome-novel-skill/issues) | 补充题材档案、文风特征库 |
| [提交 PR](https://github.com/modoojunko/awesome-novel-skill/pulls) | 修复 bug、优化代码或文档 |

### 写作风格贡献（作家）

如果你是有创作经验的作家，欢迎为反AI写作库贡献题材正反例：

**贡献内容：** `memory/anti-ai/{genre}.md` — 你所在题材的高频AI病句正反例

**贡献格式：**
```markdown
# {题材名}反AI规则

> 适用题材：{genre-id}

## 高频AI病句正反例

### 1. {问题类型}

❌ "AI味的写法"
✅ "真人感的写法"

## 写作要点

1. **{要点}** — 说明
```

**正反例原则：**
- ❌ 要具体：给真实的AI味句子，不是抽象描述
- ✅ 要可执行：给可复制的真人感写法，不是"要自然"
- 每类问题包含一对对照，同一场景、同一情绪，转化清晰

**提交方式：**
1. Fork 项目
2. 在 `memory/anti-ai/` 下新建或编辑题材文件
3. 提交 PR，标题格式：`反AI: 添加{题材名}正反例`

详细规范见 [memory/anti-ai/README.md](./memory/anti-ai/README.md)。

### 代码贡献（程序员）

**项目结构：**
```
awesome-novel-skill/
├── agents/              # 多 Agent 协作
│   ├── novel-agent.md   # 总指挥
│   ├── volume-planner.md# 叙事架构师
│   ├── chapter-planner.md# 场景设计师
│   ├── prompt-crafter.md# 提示词工程师
│   ├── writer.md        # 写手
│   ├── reader.md        # 测试读者
│   ├── updater.md       # 档案管理员
│   └── skills/          # Agent 技能 SOP
├── knowledge/            # 知识库（→ 项目 .claude/knowledge/）
│   ├── format-specs/    # 格式规范
│   └── genre-example/   # 题材案例
├── memory/               # 动态记忆（→ 项目 .claude/memory/）
│   └── anti-ai/         # 反AI写作库
└── tools/                # 工具脚本
```

**开发规范：**
- 代码遵循 PEP 8（Python）或项目既有风格
- 所有子技能修改需更新对应 SKILL.md
- 新增功能需更新 README 和 CONTRIBUTING.md

**提交方式：**
1. Fork 项目，创建功能分支
2. 提交 PR，标题格式：`类型: 简短描述`（feat/fix/refactor/docs/test）
3. PR 描述包含：改了什么、为什么改、测试方式

### Agent 技能贡献

本 Skill 由多个子技能模块组成，每个模块可独立改进：

| 模块 | 路径 | 贡献方向 |
|------|------|---------|
| Agent/Skill | `agents/` + `agents/skills/` | 改进 agent 定义、新增 skill SOP |
| 格式规范 | `knowledge/format-specs/` | 改进各环节规范文档 |
| 反AI写作库 | `memory/anti-ai/` | 新增题材正反例、丰富通用规则 |
| 题材画像 | `knowledge/genre-example/` | 新增题材档案、丰富配置内容 |

**贡献流程：**
1. 阅读目标模块的 SKILL.md 了解当前逻辑
2. 在测试项目（如有）中验证改动效果
3. 提交 PR，附上改动说明和验证结果

**Skill 贡献原则：**
- 改动需有明确的问题驱动（"因为XX问题，所以改XX"）
- 新增功能需向后兼容，不破坏现有项目
- 复杂改动先提 Issue 讨论再实现
