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
cp SKILL.md ~/.deepseek/skills/awesome-novel/
cp -r scripts ~/.deepseek/skills/awesome-novel/
```

> Claude Code 用户把路径换成 `~/.claude/skills/awesome-novel`，Hermes 用户换成 `~/.hermes/skills/awesome-novel`，OpenClaw 用户换成 `~/.openclaw/skills/awesome-novel`。

看到 "安装完成" 就可以了。

## 开始写小说

安装后，打开终端，在**你想放小说项目的目录**下启动你的 AI 工具。然后说一句：

> **帮我写本小说**

Agent 会引导你完成后续步骤。下面是你将经历的完整流程：

### 一次性设定

第一次写小说时，Agent 会和你聊这几个方面。**不用一次性想好全部**，想不到的跳过，后面随时补：

1. **题材选择** — 仙侠、都市、悬疑、历史……说你脑子里想的那个就行。Agent 会按题材类型自动配置写作风格和节奏模板
2. **世界观** — 故事发生在什么世界？有什么特殊规则？（比如"修仙世界，灵根决定天赋"）
3. **主要角色** — 主角是谁？TA 是什么样的人？Agent 会逐个角色和你讨论性格、能力、成长经历
4. **写作风格** — 偏好更偏描写还是更偏对话、更古风还是更现代？也可以导入你喜欢的小说来提取文风

### 规划故事骨架

设定聊完后，Agent 帮你规划整体故事结构：

1. **主线拆纲** — 一句话说清全书核心冲突，然后从结局倒推，拆成几个大阶段
2. **分卷规划** — 每个阶段就是一卷，每卷大概写什么、到什么位置
3. **定第一卷章节** — 第一卷分几章，每章的核心内容

> **不知道结局？** 告诉 Agent"我只知道开头"，它照样帮你规划第一卷。

### 逐章写作循环

每章按这个流程走，Agent 自动推进：

| 步骤 | 做什么 |
|------|--------|
| **① 章纲** | Agent 给出本章写作计划——写什么、分几段、情绪怎么走。你看完后说"可以"或"改一下" |
| **② 提示词** | 根据章纲和全局设定自动组装写作提示词 |
| **③ 写正文** | Agent 按提示词写完整一章 |
| **④ 审阅** | 读一遍。满意就说"归档"，不满意就说"修改第 X 段"或"重写" |
| **⑤ 归档** | 你确认后，这章正式存档。角色状态自动更新，准备下一章 |

第一章写完后，Agent 会问"下一章继续吗？"

### 自动做的事

- **去 AI 味**：生成提示词时自动净化"分析腔"，写完后检测句式重复、身体反应模板化、"不由得""不禁"等机器腔词汇，标出来让你决定要不要改
- **记伏笔**：每章结尾的情绪钩子自动追踪，该填坑的时候提醒你
- **管角色状态**：角色换了地点、变了能力、关系变了——自动记录，写下一章时 Agent 知道他的最新状态
- **节奏检查**：连续高压超过 3 章或连续平淡超过 2 章，提醒你调整

### 常用指令

| 你说 | AI 做什么 |
|------|-----------|
| "帮我写本小说" | 从头开始创建项目 + 设定讨论 |
| "帮我继续写" | 接着上次的进度继续 |
| "写下一章" | 开始写最新一章 |
| "改一下第 X 段" | 修改指定段落 |
| "这章写完了" 或 "归档" | 确认本章完成 |
| "看看进度" | 查看当前写了多少 |
| "导入这本小说" | 导入已有草稿继续写 |
| "迁移项目" | 从 2.x 旧版自动迁移到 3.0 格式 |
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

不想从头设定写作风格？项目内置 24 套题材档案，选一个就能直接开始。每套档案包含角色人设倾向、叙事语气和章节提示词模板。涵盖仙侠、都市、悬疑、历史、科幻末世、西方奇幻等主流类型。

Agent 会在设定阶段问你要不要选。

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

默认配置就是"低 AI 味"——禁止了常见机器腔句式（"不由得""不禁""就在这时""不是 X 而是 Y"分析腔）、强制短句长句交替、禁止身体反应模板化。写完后还会自动扫描检测。

**Q: 可以用自己的写作风格吗？**

可以。项目创建后有专门的写作风格文件，你可以把自己的偏好写进去，后面所有章节都会按这个风格来。

## Star History

<a href="https://star-history.com/#modoojunko/awesome-novel-skill">
  <img src="https://api.star-history.com/svg?repos=modoojunko/awesome-novel-skill&type=date" alt="Star History">
</a>

## 致谢

感谢 [@hust-open-atom-club](https://github.com/hust-open-atom-club) 的 [DeepSeek TUI](https://github.com/hust-open-atom-club/DeepSeek-TUI) 项目为 DeepSeek V4 用户提供免费、流畅的终端体验，让本 Skill 对个人用户完全免费可用。

本项目部分设计受到 [InkOS](https://github.com/Narcooo/inkos) 的启发——包括 AI 味检测体系、伏笔/钩子追踪、题材配置和分层技法模型。感谢 [@Narcooo](https://github.com/Narcooo) 的优秀工作。
