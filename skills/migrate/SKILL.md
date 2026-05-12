---
name: novel-migrate
description: 旧版项目迁移。Step 1 检测到 story.yaml 或 skill_version 过低时分发至此。将 2.x 格式的 YAML 设定→Markdown，挪入 old/ 回滚保留。仅已归档章节迁移，在制章节跳过。
---

# 迁移子技能

> 作者工作流从 2.x 升级到 3.0 时的自动迁移机制。作者可以在旧版本工作空间中升级技能后直接继续创作。

**模型：** haiku（主 agent 编排），sonnet（subagent 做字段映射）

## 范围 Scope

### 做什么
- 将旧版 2.x 项目的 YAML 设定文件迁移到新版 Markdown 格式
- 已归档章节的正文直接拷贝
- 已归档章纲的 YAML→Markdown 格式转换
- 废弃文件的清理

### 不做什么
- ❌ 不迁移在制章节（非 archived）
- ❌ 不修改正文内容（纯拷贝）
- ❌ 不改写提示词内容（纯拷贝）
- ❌ 不处理 git 冲突（假设工作目录干净）
- ❌ 不恢复已删除的废弃文件
- ❌ 不创建新章节/新卷

### 边界条件
- 如果 `old/` 目录已存在 → 使用 `old-2/`、`old-3/` 递增
- 如果 `scripts/init.py` 不可用 → 手动创建目录结构 + 复制模板
- 如果旧 `story.yaml` 缺少 title 或 author → 用目录名作标题，author 留空
- 如果 volumes/ 下无 yaml → story.md 分卷规划标"待补充"

## 工具契约 Tools

| 工具 | 用途 | 限制 |
|------|------|------|
| Bash | 执行 shell 命令（文件搬移/拷贝/检测） | 不安装新包，不改系统配置 |
| Read | 读旧 YAML 文件、读模板 | — |
| Write/Edit | 写新 Markdown 文件 | 不写 old/ 目录内的文件 |
| Agent | 启动并行 subagent 做设定迁移 | 仅 Step 4 使用，subagent 只能用 Read/Write/Edit |

## 生命周期 Lifecycle

### Start
执行任何操作前，读 `.agent/status.md`（如果存在），确认 `migrated` 标志。如果已标记为 migrated → 跳过迁移，分发回报文"该项目已迁移"。

### End
迁移完成后，更新 `.agent/status.md`：
```markdown
# Status

- **migrated:** true
- **migrated_at:** {当前时间}
- **old_version:** "2.x"
- **new_version:** "3.0"
- **skipped_chapters:** [在制章节列表]
- **pending_fields:** [待补充字段列表]
```

## 版本检测

| 信号 | 结论 |
|------|------|
| `story.yaml` 存在 && `story.md` 不存在 | **v2.x 旧版** → 需要迁移 |
| `story.md` 存在但 `skill_version` < 当前技能版本 | **待升级迁移** → 需要迁移 |
| `story.md` 存在且 `skill_version` >= 当前版本 | **新版** → 正常流程，不分发至此 |
| 无任何文件 | **全新项目** → 分发到 novel-setup |

检测命令：

```bash
# 旧版检测
test -f story.yaml && test ! -f story.md && echo "v2.x"
# 版本检测
grep -q "skill_version" story.md && echo "has_version" || echo "needs_update"
```

## SOP 总览

主 Agent 执行 7 步流程，其中 Step 4（设定迁移）拆为多个并行 subagent 执行：

```
Step 0 ─ 检测版本 → 决策是否进入迁移
  │
Step 1 ─ 展示迁移计划 + 作者确认
  │
Step 2 ─ 整体挪入 old/
  │
Step 3 ─ 初始化新骨架（init.py）
  │
Step 4 ─ 迁移设定 ←── 并行 subagent
  ├── subagent A: 5.1 story.yaml → story.md
  ├── subagent B: 5.2 world-setting.yaml → world-setting.md
  ├── subagent C: 5.3 writing-style + 5.8 genre-setting
  ├── subagent D: 5.4 anti-ai + 5.5 hooks → foreshadowing
  ├── subagent E: 5.6 角色 yaml → character-setting/*.md
  ├── subagent F: 5.7 volume yaml → volume-{N}.md
  └── subagent G: 5.9 chapter yaml → chapter.md（已归档）
  │
Step 5 ─ 拷贝正文（archives/ + prompts/）
  │
Step 6 ─ 验收 + 汇报
```

## 前置条件

- 项目目录下的 `.claude/`、`.deepseek/`、`CLAUDE.md`、`.git/`、`install.sh`、`.gitignore` **不会**被挪动
- 本技能自身的文件（`SKILL.md`、`scripts/`、`references/`、`skills/`）在项目根目录之外，不受影响
- `scripts/init.py` 必须可用（用于 Step 3 骨架初始化）

---

## Step 0：检测

```bash
ls story.yaml story.md 2>/dev/null
```

- `story.yaml` 存在 + `story.md` 不存在 → **旧版**，继续 Step 1
- `story.md` 存在 → 读 `story.md` 头部 `skill_version`，若 < 当前版本 → **待升级**，继续 Step 1
- 两者都不存在 → **全新项目**，分发到 novel-setup（退出本技能）

## Step 1：展示迁移计划 + 作者确认 [硬节点]

扫描项目目录，给作者看三张清单：

**文件清单**（自然语言描述，不需完整遍历）：
- 设定文件：story.yaml + settings/ 下所有 yaml
- 角色文件：settings/character-setting/ 下所有 yaml
- 卷纲：volumes/ 下所有 yaml
- 正文：archives/ 下 `.md` 文件数量
- 章纲（已归档）：chapters/ 下 `status=archived` 的章节数量
- 章纲（跳过）：chapters/ 下 `status!=archived` 的章节标题和状态
- 提示词：prompts/ 下文件数量

**废弃文件清理**（直接丢弃，不挪入 old/）：
- `author-intent.md`、`current-focus.md`
- `drafts/`、`drifts/`、`tmp/`、`temp-*.txt`
- `manuscripts/`、`.vscode/`

格式示例：

```
以下文件将迁移：
  → 设定：story.yaml, settings/world-setting.yaml, settings/writing-style.yaml ...
  → 角色：settings/character-setting/（N 个角色）
  → 卷纲：volumes/volume-1.yaml ...（N 卷）
  → 正文：archives/*.md（N 篇）
  → 章纲（已归档）：chapters/vol-*-ch-*.yaml（N 篇）
  → 提示词：prompts/（N 个）

以下章节将跳过（在制过程）：
  → chapters/vol-3-ch-4.yaml（status=draft）
  → chapters/vol-3-ch-5.yaml（status=outline）

以下废弃文件将清理：
  → author-intent.md, current-focus.md, drafts/, drifts/, manuscripts/, tmp/

开始迁移？
```

**作者确认后才继续。** 作者说"可以"或"开始"则继续。

## Step 2：整体挪入 old/

```bash
# 确认 old/ 名唯一
if [ -d old ]; then
  suffix=2
  while [ -d "old-$suffix" ]; do suffix=$((suffix+1)); done
  mv old "old-$suffix"
fi

mkdir old
mv story.yaml old/
mv settings/ old/
mv volumes/ old/
mv chapters/ old/
mv archives/ old/
mv prompts/ old/
```

**废弃文件直接删除**（不挪入 old/）：
```bash
rm -rf author-intent.md current-focus.md temp-*.txt drafts/ drifts/ manuscripts/ tmp/ .vscode/
```

**不动的内容：** `.claude/`、`.deepseek/`、`CLAUDE.md`、`.git/`、`install.sh`、`.gitignore`

## Step 3：初始化新骨架

```bash
# 从旧 story.yaml 读取标题和作者
TITLE=$(grep "^title:" old/story.yaml | head -1 | sed 's/^title: *"//;s/"$//')
AUTHOR=$(grep "^author:" old/story.yaml | head -1 | sed 's/^author: *"//;s/"$//')

python3 "$SKILL_DIR/scripts/init.py" "$(pwd)" --author "$AUTHOR"
```

`init.py` 生成完整 3.0 骨架：

```
├── story.md（含 skill_version: 3.0 占位）
├── settings/
│   ├── world-setting.md（模板）
│   ├── writing-style.md（模板）
│   ├── genre-setting.md（模板）
│   ├── anti-ai.md（模板）
│   ├── hooks.md（模板）
│   ├── foreshadowing.md（模板）
│   └── character-setting/（空）
├── volumes/（空）
├── chapters/（空）
├── archives/（空）
└── prompts/（空）
```

如果 `init.py` 不支持直接传入路径作为项目名（即只能创建新目录），Agent 在项目目录下执行 `init.py .` 或手动补建缺失目录和文件。

## Step 4：迁移设定（并行 subagent）

主 Agent 启动多个并行 subagent，每个负责一个迁移子步骤。subagent 之间的工作互不依赖，可以全部同时启动。

**模型：** sonnet（字段映射需要质量）

每个 subagent 的通用指令框架：

```
你是一个迁移 subagent。你的任务是将 [{文件名}] 从旧版 YAML 格式迁移到新版 Markdown 格式。

旧文件路径：old/{路径}
新文件路径：{路径}
模板路径：{模板路径}
字段映射：见 references/migration-spec.md §{节号}

执行步骤：
1. 读旧 YAML 文件
2. 读模板文件
3. 按 §{节号} 的字段映射表逐字段迁移
4. 写新文件
5. 回答：迁移完成 + 遇到什么问题（如有）
```

### 4a — story.yaml → story.md（§1）

| 输入 | 路径 |
|------|------|
| 旧文件 | `old/story.yaml` |
| 旧卷纲 | `old/volumes/*.yaml` |
| 模板 | `scripts/templates/story.md.template` |
| 输出 | `story.md` |

关键操作：
- 从旧 story.yaml 提取 title/author/created_at
- 从 `old/volumes/` 下每个 yaml 读取 title/core_conflict
- 填充引用路径表、故事主线（从各卷归纳）、分卷规划
- 写入 `skill_version: 3.0`

### 4b — world-setting.yaml → settings/world-setting.md（§2）

| 输入 | 路径 |
|------|------|
| 旧文件 | `old/settings/world-setting.yaml` |
| 模板 | `scripts/templates/world-setting.md.template` |
| 输出 | `settings/world-setting.md` |

关键操作：8 个旧自由文本字段（geography/politics/culture/history/rules/physics/biology/sociology）→ 3 大节（地理/政治/规则）各含子字段。Agent 读旧文本理解后归纳填入新版结构化位置。

### 4c — writing-style.yaml + genre-setting（§3 + §8）

| 输入 | 路径 |
|------|------|
| 旧文件 | `old/settings/writing-style.yaml` |
| 模板 | `scripts/templates/writing-style.md.template` |
| 模板 | `scripts/templates/genre-setting.md.template` |
| 输出 | `settings/writing-style.md` + `settings/genre-setting.md` |

关键操作：
- writing-style 基本 1:1 迁移（旧模板和旧内容结构一致）
- 从旧版 `genre_profile` 填入选定类型；如果旧版有 genre 段的 satisfaction_types/pacing_rules/anti_cliches，一并填入 genre-setting.md

### 4d — anti-ai.yaml + hooks.yaml（§4 + §5）

| 输入 | 路径 |
|------|------|
| 旧文件 | `old/settings/anti-ai.yaml` |
| 旧文件 | `old/settings/hooks.yaml` |
| 模板 | `scripts/templates/anti-ai.md.template` |
| 模板 | `scripts/templates/foreshadowing.md.template` |
| 输出 | `settings/anti-ai.md` + `settings/foreshadowing.md` |

关键操作：
- anti-ai：新版分类更清晰（副词/动词/形容词/连接词/身体反应），从旧版 fatigue_words_zh 按类别填入
- foreshadowing：hooks.yaml → 三张摘要表（活跃/已收束/废弃）

### 4e — 角色 yaml → character-setting/*.md（§6）

| 输入 | 路径 |
|------|------|
| 旧文件 | `old/settings/character-setting/*.yaml`（全部） |
| 模板 | `scripts/templates/character.md.template` |
| 输出 | `settings/character-setting/*.md`（每个角色一个） |

关键操作：
- 对 `old/settings/character-setting/` 下每个 yaml：
  - name → 名称, story_role → 故事角色, appearance → 外貌
  - background + summary + age + occupation → 背景
  - cognition 6 层 → 认知 6 层模型
  - relationships → 关系
  - state_history → 状态历史
  - 语言特征和情绪弧线标"待补充"（旧版无此字段）

### 4f — volume yaml → volumes/volume-{N}.md（§7）

| 输入 | 路径 |
|------|------|
| 旧文件 | `old/volumes/*.yaml`（全部） |
| 模板 | `scripts/templates/volume.md.template` |
| 输出 | `volumes/volume-{N}.md`（每卷一个） |

关键操作：title → 标题, core_conflict → 核心冲突, chapters_summary → 章节列表

### 4g — chapter yaml → chapter.md（仅 archived，§9）

| 输入 | 路径 |
|------|------|
| 旧文件 | `old/chapters/*.yaml`（仅 status=archived） |
| 模板 | `scripts/templates/chapter.md.template` |
| 输出 | `chapters/vol-{N}-ch-{M}.md` |

关键操作：
1. 筛选：读每个 yaml 的 `status` 字段，只处理 `archived`
2. 映射：按 §9 字段映射表转换
3. 特殊处理：
   - `narrative_pov` → Memo→当前任务 末尾，标记 `[视角]`
   - `narrative_style` → Memo→当前任务 末尾，标记 `[风格]`
   - `segments` → 跳过
   - `cycle_position`/`suppression_stack` → 跳过
   - 无数据的字段 → 标"（待补充）"，不捏造

### 并行执行策略

主 Agent 一次启动全部 7 个 subagent。subagent 之间无依赖关系，可全速并行。

每个 subagent 的工作量估计：
- 4a（story.md）：小，1 文件 + 少量归纳
- 4b（world-setting）：中，1 文件 + 归纳提炼
- 4c（writing-style + genre）：小，基本 1:1 复制
- 4d（anti-ai + foreshadowing）：中，2 文件
- 4e（characters）：按角色数量线性增长
- 4f（volumes）：小，按卷数
- 4g（chapters）：最大，按章节数量线性增长

如果 subagent 数量受限，优先级：4e > 4g > 4b > 4d > 4a > 4c > 4f

## Step 5：拷贝正文

```bash
# archives/ — 直接复制 .md
cp old/archives/*.md archives/
# 不复制 .draft.md 文件（未归档）

# prompts/ — 直接复制
cp old/prompts/*.md prompts/
cp old/prompts/*.txt prompts/ 2>/dev/null
```

正文不做任何修改。提示词保留原文件名：
- `vol-{N}-ch-{M}-prompt.md` — 新版兼容命名
- `vol-{N}-ch-{M}-seg-{S}-prompt.md` — 旧版分段命名，也保留

## Step 6：验收 + 汇报

### 结构验收

逐项检查：

```
□ story.md 存在，skill_version = 3.0
□ settings/world-setting.md 存在且已填充（非模板状态）
□ settings/writing-style.md 存在且已填充
□ settings/genre-setting.md 存在
□ settings/anti-ai.md 存在
□ settings/foreshadowing.md 存在（hooks 摘要）
□ settings/character-setting/ 每角色一个 .md 文件
□ volumes/ 卷数与旧版一致
□ chapters/ 所有 archived 章节已迁移
□ archives/ 正文全部复制
□ prompts/ 提示词全部复制
□ 旧 .yaml 文件已移入 old/（无残留）
□ 废弃文件已清理
```

### 汇报格式

```
迁移完成。
──────────────────────────────
✅ 成功完成（N 项）：
  - story.md → 标题/作者/3卷规划
  - world-setting.md → 已填充
  - 角色 → N 个角色
  - 卷纲 → N 卷
  - 章纲 → N 篇 archived 章节
  - 正文 → N 篇
  - 提示词 → N 个

⏭️ 跳过（N 项）：
  - chapters/xxx（status=draft）
  - chapters/xxx（status=outline）

📌 待补充字段：
  - settings/world-setting.md → 个人级规则
  - settings/character-setting/*.md → 语言特征、情绪弧线
  - settings/genre-setting.md → 满足类型、节奏规则、避免套路、类型禁忌

──────────────────────────────
old/ 目录保留了所有旧文件，确认迁移无误后可以手动 rm -rf old/ 删除。
```

汇报中必须列出跳过的章节和待补充的字段，让作者知道迁移后的文件状态，知悉哪些内容需要后续完善。

## Definition of Done

本技能执行完毕的标志（满足全部）：

1. ✅ 所有旧 YAML 已移入 `old/`，无残留
2. ✅ `story.md` 存在，`skill_version = 3.0`
3. ✅ 设定文件全部迁移完毕（world-setting / writing-style / genre-setting / anti-ai / foreshadowing）
4. ✅ 所有角色各有一个 `.md` 文件
5. ✅ 卷纲数量与旧版一致
6. ✅ 所有 archived 章纲已迁移
7. ✅ 正文全部拷贝
8. ✅ 提示词全部拷贝
9. ✅ 废弃文件已清理
10. ✅ `.agent/status.md` 已更新 `migrated: true`
11. ✅ 验收汇报已展示给作者

有一个不满足就不算 done。如果不满足可修复则修复后继续；不可修复（如旧文件损坏）→ 上报作者。
