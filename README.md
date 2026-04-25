# Novel Agent Skill

人类与AI协作写小说的工作流系统

## 功能

- 初始化小说项目目录结构
- 引导作者一步步完成世界设定、角色设定
- 讨论卷、章故事线并生成章纲
- 生成高质量提示词，调用subagent写正文
- 归档完成的章节，自动更新角色状态

## 安装

### Claude Code

```bash
# 克隆或复制项目
git clone https://github.com/modoojunko/awesome-novel-skill.git
cd awesome-novel-skill

# 安装为全局 skill
cp -r . ~/.claude/skills/novel-agent/

# 或创建符号链接
ln -s "$(pwd)" ~/.claude/skills/novel-agent
```

安装后在 Claude Code 中使用：
```
/novel-agent
```
或直接开始创作小说。

### OpenClaw

```bash
# 参考 OpenClaw 的 skill 安装文档
# 通常将项目路径配置为 skill 来源
openclaw skill add file:///path/to/awesome-novel-skill
```

### Hermes

```bash
# 参考 Hermes 的 skill 安装文档
# 通常将项目路径配置为 skill 来源
hermes skill install /path/to/awesome-novel-skill
```

## 使用

### 1. 创建新项目

```
create novel 我的小说
cd 我的小说
```

init命令会创建：
```
我的小说/
├── story.yaml
├── settings/
│   ├── world-setting.yaml
│   ├── character-setting/
│   └── writing-style.yaml
├── volumes/
├── chapters/
└── archives/
```

### 2. 设定阶段

Agent引导作者讨论：
- 世界设定（地理、政治、文化、历史、规则等）
- 角色设定（每个角色一个yaml，包含cognition、worldview、self_identity、values、abilities、skills、environment）

### 3. 故事线拆分

- 讨论卷、章的故事线拆分
- 每卷的卷纲
- 每章的章纲

### 4. 正文生成

- Agent生成提示词yaml
- 作者审批提示词
- Agent调用subagent写正文
- 作者审阅并修改

### 5. 归档

- 正文满意后归档为markdown
- Agent自动更新角色状态

## 项目结构

```
novel-project/
├── story.yaml                    # 核心索引
├── settings/
│   ├── world-setting.yaml       # 世界设定
│   ├── character-setting/       # 角色设定
│   │   ├── protagonist.yaml
│   │   └── antagonist.yaml
│   └── writing-style.yaml       # 写作风格
├── volumes/
│   └── volume-1.yaml
├── chapters/
│   ├── vol-1-ch-1.yaml
│   └── prompts/                 # 提示词
│       └── vol-1-ch-1-prompt.yaml
└── archives/
    └── vol-1-ch-1-title.md
```

## 授权模式

- **步步授权（默认）**: 每步需作者确认
- **全部授权**: Agent全权决定，作者只在最终结果审阅

作者可随时说"你全权决定"或"每步都要我确认"切换模式。

## 工作流文件

- 过程文件: YAML格式
- 最终归档: Markdown格式
- 命名规范: `vol-{N}-ch-{M}-{slugified-title}.md`
