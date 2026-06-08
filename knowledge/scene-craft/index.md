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
├── appearance/                   # 角色外貌描写
│   └── universal.md
├── inner-mono/                   # 心理活动/内心独白
│   └── universal.md              # ✅ 生理通感/思维碎片/递进崩塌
├── group-scene/                  # 群像场景（待补充）
│   └── universal.md
└── transition/                   # 过渡场景（待补充）
    └── universal.md
```

## 标签系统

每个场景类型文件中的技法条目以 `[标签]` 开头。标签是 prompt-crafter 选取时的筛选依据：

```
## [权力] 权力动态——谁主导谁防守
## [潜台词] 错位——台词和动作不一致
## [节奏] 节奏变化
## [信息差] 信息差驱动对话
```

prompt-crafter 加载文件后，不全部注入 L8——根据场景核心事件匹配标签，只选取相关的 2-4 条。

### 标签匹配逻辑

```
L5 场景核心事件："方岩在办公室回避陆征的追问"
  → 触发标签：[隐瞒]、[权力]、[潜台词]
  → 从 dialogue/universal.md 选取这三条 → 四步转化 → L8

L5 场景核心事件："两个角色在街头闲聊"
  → 触发标签：无直接冲突标签
  → 从 dialogue/universal.md 选取[动作]、[区分] → 四步转化 → L8
```

优先级：匹配标签的技法 > 无标签的通用技法。

## 加载方式

prompt-crafter 根据 L5 识别的场景类型，按以下路径读取：

1. 通用方法论：`scene-craft/{类型}/universal.md`
2. 题材特化：`scene-craft/{类型}/{当前题材}.md`（存在则读，否则跳过）

通用方法论 + 题材特化合并 → 按标签筛选 → 四步转化 → 注入 L8。
