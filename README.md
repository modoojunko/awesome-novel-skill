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

打开终端，在你想放小说的目录下启动你的 AI 编程工具（Claude Code / Hermes / OpenClaw），比如：

```bash
cd ~/我的小说
claude
```

然后对你的 AI Agent 说：

> **create novel 我的第一本小说**

Claude 会在当前目录下创建一个以你小说命名的文件夹，然后引导你按以下流程进行：

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
