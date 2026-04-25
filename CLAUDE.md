# Novel Agent Skill

人类与AI协作写小说的工作流系统。

## 项目结构

```
awesome-novel-skilll/
├── SKILL.md          # Agent 默认加载的 skill 定义
├── CLAUDE.md         # 本文件，项目级指导
├── README.md         # 用户文档
├── scripts/
│   ├── init.py       # 项目初始化脚本
│   └── templates/    # YAML 模板文件
│       ├── story.yaml.template
│       ├── world-setting.yaml.template
│       ├── character.yaml.template
│       ├── volume.yaml.template
│       ├── chapter.yaml.template
│       └── writing-style.yaml.template
└── docs/            # 设计文档
```

## 核心流程

1. **Init**: `create novel [项目名]` → 创建目录结构
2. **设定阶段**: 讨论世界设定 + 角色设定
3. **故事线拆分**: 卷、章的拆解和章纲确认
4. **提示词生成**: 生成3个选项供选择
5. **正文生成**: subagent 一次生成完整章节
6. **归档**: 写入 markdown + 更新角色状态

## 关键文件

- `SKILL.md` - skill 定义，包含完整工作流
- `story.yaml` - 小说项目核心索引
- `settings/writing-style.yaml` - 写作风格指南

## 使用方式

直接使用此 skill：

```bash
cd /path/to/awesome-novel-skilll
claude
```

## 与 Skill 交互

此项目作为 agent skill 使用，SKILL.md 包含所有工作流定义。
