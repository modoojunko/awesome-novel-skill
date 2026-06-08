# 场景写作方法论

> 按场景类型组织的小说写法指南。每场景一个目录，内含通用方法论 + 各题材特化覆盖。

## 目录结构

```
scene-craft/
├── index.md                      # 索引
├── dialogue/                     # 对话场景
│   ├── universal.md              #   通用对话方法论
│   ├── xianxia.md                #   仙侠题材特化
│   └── suspense-crime.md         #   悬疑刑侦特化
├── fight/                        # 战斗/对抗
│   ├── universal.md              #   通用战斗方法论
│   ├── xianxia.md                #   仙侠题材特化
│   └── suspense-crime.md         #   悬疑刑侦特化
├── environment/                  # 环境/氛围描写
│   ├── universal.md              #   通用方法论（待补充）
│   ├── xianxia.md                #   仙侠题材特化
│   └── suspense-crime.md         #   悬疑刑侦特化
├── inner-mono/                   # 心理活动（待补充）
│   └── universal.md
├── group-scene/                  # 群像场景（待补充）
│   └── universal.md
└── transition/                   # 过渡场景（待补充）
    └── universal.md
```

## 加载方式

prompt-crafter 根据 L5 识别的场景类型，按以下路径读取：

1. 通用方法论：`scene-craft/{类型}/universal.md`
2. 题材特化：`scene-craft/{类型}/{当前题材}.md`（存在则读，否则跳过）

通用方法论 + 题材特化合并 → 经四步转化法 → 注入 L8。
