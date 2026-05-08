# Novel Agent — 和 AI 一起写小说

让 Claude 成为你的小说创作搭档。从世界观搭建到角色塑造，从章节规划到正文写作，一步步陪你完成整部小说。

## 你需要什么

- 安装了以下任一工具的电脑：[Claude Code](https://docs.anthropic.com/zh-CN/docs/claude-code/overview)、[Hermes](https://github.com/hermes/hermes) 或 [OpenClaw](https://github.com/openclaw/openclaw)
- 大概 1 分钟完成安装

## 安装

根据你用的工具，复制对应那行命令，在终端里粘贴执行：

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

如果上面那行不行，手动来（也是复制粘贴，以 Claude Code 为例）：

```bash
git clone https://github.com/modoojunko/awesome-novel-skill.git
cd awesome-novel-skill
mkdir -p ~/.claude/skills/awesome-novel
cp SKILL.md ~/.claude/skills/awesome-novel/
cp -r scripts ~/.claude/skills/awesome-novel/
```

> Hermes 用户把路径换成 `~/.hermes/skills/awesome-novel`，OpenClaw 用户换成 `~/.openclaw/skills/awesome-novel`。

看到 "安装完成" 就可以了。

## 开始写小说

打开终端，在你想放小说的目录下启动你的 AI 编程工具（Claude Code / Hermes / OpenClaw），然后用自然语言告诉它你想做什么。比如：

> **我想写一本玄幻小说，帮我开始**

> **来帮我写小说吧**

Agent 会在当前目录下创建小说项目，然后引导你按以下流程进行：

### 第一步：设定世界观

Claude 会问你几个问题——这是什么类型的故事（玄幻？科幻？悬疑？），然后逐项和你讨论这个世界的细节：地理长什么样、政治格局如何、有什么特殊规则……就像和一个编辑聊天，聊完它帮你整理好。

### 第二步：设计角色

然后设计人物。你说出角色名，Claude 一个一个和你讨论：
- 这个人的性格和价值观
- 他的能力和特长
- 他的成长经历

也是聊完就整理好。

### 第三步：规划章节

世界观和角色都有了，开始规划故事走向。先分卷，再分章。Claude 会和你讨论每一章要写什么——核心情节是什么、哪些角色出场、发生在什么场景。

### 第四步：生成正文

每一章讨论完章纲后，Claude 会准备好写作材料，然后开始写正文。写完一章给你看，你觉得哪里不好可以直接说，它帮你改。

### 第五步：存档

正文满意了，Claude 会把它存档，同时自动更新角色状态——比如角色在这一章里突破了境界、换了地点、和谁结了仇，这些都会记录下来，下一章写的时候自动用上。

### 过程中自动做的事

- **去 AI 味**：写完后自动检测"机器腔"——句式开头重复、身体反应模板化（"眼神一暗""心里一沉"用太多）、公式化副词（"不由得""不禁"）、"不是X而是Y"分析句式，有就标出来让你决定要不要改。生成提示词时还会自动净化，防止 AI 分析腔渗入正文
- **记伏笔**：你埋下的每个伏笔、每章结尾的情绪钩子，自动追踪——该填坑的时候提醒你
- **管角色状态**：角色换了地方、变了能力、关系变了，都自动记下来，写下一章时 Claude 知道他的最新状态
- **节奏检查**：连续高压章节超过 3 章、连续平淡超过 2 章，提醒你调整

### 更高阶的玩法

**用预置题材画像快速启动**

不想从头设定写作风格？项目内置了 4 套类型档案，选一个就能直接开始。每套档案包含角色人设、叙事语气和章节提示词模板：

- **古代权谋** — 庙堂博弈、世家大族、制度性压抑下的个人选择
- **科幻末世** — 废土生存、文明重建、末日伦理困境
- **悬疑犯罪** — 刑侦推理、社会派悬疑、证据链驱动的节奏控制
- **都市言情** — 日常生活的情感递进，以细节和动作传达情绪

Claude 会在设定阶段问你要不要选一个，选了之后所有章节自动注入对应的写作风格。

**从喜欢的小说里学文风**

有没有特别喜欢的小说，想让 Claude 照着那个风格写？用文风提取功能：

1. 把参考小说文件放进项目目录
2. 跟 Claude 说"分析一下这本小说的文风"
3. Claude 会跑统计分析（句子长短、对话占比、描写密度），再定性提取风格特征，最后输出一份风格档案给你确认
4. 确认后自动合并到你的写作配置里，后续所有章节按这个风格写

## 两种协作模式

- **步步确认**（默认）：每做一步，Claude 都等你点头才继续
- **全部授权**：你说"你全权决定"，Claude 就自己往下走，完工了再给你看

两种模式随时可以切换，跟 Claude 说一声就行。

## 常见问题

**Q: 我不会编程，能装吗？**

能。上面那几行命令复制粘贴到终端，回车就行。唯一的前提是你的电脑上已经装好了 Claude Code、Hermes 或 OpenClaw。

**Q: 写到一半可以改设定吗？**

可以。随时跟 Claude 说"改一下世界观里的xxx"或"这个角色的性格我想调整"，它会帮你更新。

**Q: 生成的文章质量怎么样？**

Claude 会严格按照你确认的世界观、角色设定和写作风格来写。你对风格的偏好（更偏描写还是更偏对话、更古风还是更现代）都可以在设定阶段告诉它。

**Q: 可以用自己的写作风格吗？**

可以。项目创建后有个写作风格文件，你可以把自己的风格偏好写进去，之后所有章节都会按这个风格来。

**Q: 生成的文字有 AI 味怎么办？**

默认写作风格就是"低 AI 味"配置——禁止了常见的机器腔句式（"不由得""不禁""就在这时""不是X而是Y"分析腔）、强制短句长句交替、禁止身体反应模板化。写完后还会自动扫描检测，发现 AI 味重的地方会标出来让你改。提示词生成时也会自动净化 what_to_write，防止 AI 分析腔渗入正文。

## 📈 Stats
## Star History

<a href="https://www.star-history.com/?type=date&repos=modoojunko%2Fawesome-novel-skill">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=modoojunko/awesome-novel-skill&type=date&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=modoojunko/awesome-novel-skill&type=date&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=modoojunko/awesome-novel-skill&type=date&legend=top-left" />
 </picture>
</a>

## 致谢

本项目部分设计受到 [InkOS](https://github.com/Narcooo/inkos) 的启发——包括 AI 味检测体系、伏笔/钩子追踪、题材配置和分层技法模型。感谢 [@Narcooo](https://github.com/Narcooo) 的优秀工作。
