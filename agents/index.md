# Agent Index

主 Agent 根据当前阶段查此表决定派谁。Agent ID 用于 task registry 映射。

## 圆桌 Agent（讨论用）

### 设定阶段

| Agent ID | 名称 | 文件 | 职责 | 产出 |
|----------|------|------|------|------|
| `geographer` | 地理师 | `roundtable/setting/geographer.md` | 问作者地理/气候/资源 | 问答记录 |
| `politician` | 政治师 | `roundtable/setting/politician.md` | 问作者权力/制度/势力 | 问答记录 |
| `culturist` | 文化师 | `roundtable/setting/culturist.md` | 问作者信仰/习俗/日常 | 问答记录 |
| `power-system` | 力量体系师 | `roundtable/setting/power-system.md` | 问作者超自然规则/边界 | 问答记录 |
| `character-designer` | 角色师 | `roundtable/setting/character-designer.md` | 问作者人物/动机/关系 | 问答记录 |

### 卷纲阶段

| Agent ID | 名称 | 文件 | 职责 | 产出 |
|----------|------|------|------|------|
| `volume-structure` | 结构师（宏观） | `roundtable/volume-outline/structure.md` | 问全卷骨架/分章/高潮 | 卷方案 |
| `volume-theme` | 主题师 | `roundtable/volume-outline/theme.md` | 问主题递进/深化 | 卷方案 |
| `volume-character-arc` | 人物弧线师 | `roundtable/volume-outline/character-arc.md` | 问角色成长线 | 卷方案 |
| `volume-hook-planner` | 钩子规划师 | `roundtable/volume-outline/hook-planner.md` | 问跨卷钩子/悬念 | 卷方案 |
| `volume-pace` | 节奏师 | `roundtable/volume-outline/pace.md` | 问松紧分布/节奏 | 卷方案 |

### 章纲阶段

| Agent ID | 名称 | 文件 | 职责 | 产出 |
|----------|------|------|------|------|
| `chapter-structure` | 结构师（微观） | `roundtable/chapter-outline/structure.md` | 出章内结构方案 | 章方案 |
| `chapter-character-driver` | 人物驱动师 | `roundtable/chapter-outline/character-driver.md` | 出POV/弧光方案 | 章方案 |
| `chapter-hook-manager` | 钩子管理师 | `roundtable/chapter-outline/hook-manager.md` | 出每章钩子方案 | 章方案 |
| `chapter-emotion-designer` | 情绪设计师 | `roundtable/chapter-outline/emotion-designer.md` | 出情绪曲线方案 | 章方案 |
| `chapter-setting-guardian` | 设定守门员 | `roundtable/chapter-outline/setting-guardian.md` | 出边界检查方案 | 章方案 |

### 段拆分阶段

| Agent ID | 名称 | 文件 | 职责 | 产出 |
|----------|------|------|------|------|
| `segment-structure` | 段结构师 | `roundtable/segment/structure.md` | 出分段方案 | 段方案 |
| `segment-viewpoint` | 视角师 | `roundtable/segment/viewpoint.md` | 出POV分配方案 | 段方案 |
| `segment-plot-pace` | 剧情节奏师 | `roundtable/segment/plot-pace.md` | 出段内剧情方案 | 段方案 |
| `segment-micro-emotion` | 情绪微设计师 | `roundtable/segment/micro-emotion.md` | 出每段情绪方案 | 段方案 |
| `segment-hook-distributor` | 钩子分配师 | `roundtable/segment/hook-distributor.md` | 出钩子落段方案 | 段方案 |

## 流水线 Agent（执行 + 验收）

| 阶段 | 类型 | Agent ID | 文件 | 职责 |
|------|------|----------|------|------|
| 1 | 执行 | `exec-init` | `pipeline/exec-init.md` | 建目录结构 + story.yaml + writing-style预填 |
| 1 | 验收 | `review-init` | `pipeline/review-init.md` | 检查目录完整性 |
| 2 | 执行 | `exec-world` | `pipeline/exec-world.md` | 写 world-setting.yaml |
| 2 | 执行 | `exec-character` | `pipeline/exec-character.md` | 写 character/*.yaml |
| 2 | 执行 | `exec-style` | `pipeline/exec-style.md` | 补完 writing-style.yaml |
| 2 | 执行 | `exec-hook` | `pipeline/exec-hook.md` | 写 hooks.yaml |
| 2 | 执行 | `exec-meeting-notes` | `pipeline/exec-meeting-notes.md` | 写 author-intent.md |
| 2 | 验收 | `review-setting` | `pipeline/review-setting.md` | 检查设定一致性 |
| 3.1 | 执行 | `exec-volume` | `pipeline/exec-volume.md` | 写 volume.yaml |
| 3.2 | 执行 | `exec-outline` | `pipeline/exec-outline.md` | 写 chapter.yaml |
| 3.2 | 验收 | `review-outline` | `pipeline/review-outline.md` | 检查章纲 |
| 3.3 | 执行 | `exec-segment` | `pipeline/exec-segment.md` | 段拆分落盘 |
| 4 | 执行 | `exec-prompt` | `pipeline/exec-prompt.md` | 组装提示词 |
| 4 | 验收 | `review-prompt` | `pipeline/review-prompt.md` | 检查提示词 |
| 5 | 执行 | `exec-prose` | `pipeline/exec-prose.md` | 写正文 |
| 5 | 执行 | `exec-stitch` | `pipeline/exec-stitch.md` | 缝合segment |
| 5 | 执行 | `exec-de-ai` | `pipeline/exec-de-ai.md` | 去AI味 |
| 5 | 验收 | `review-prose` | `pipeline/review-prose.md` | 检查正文 |
| 6 | 执行 | `exec-archive` | `pipeline/exec-archive.md` | 归档 |
| 6 | 验收 | `review-archive` | `pipeline/review-archive.md` | 检查归档 |
