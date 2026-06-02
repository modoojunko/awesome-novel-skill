---
name: migrator
description: 旧版项目迁移 SOP——7 步完整流程：检测→展示计划→备份→初始化→迁移→拷贝→验收
---

# migrator skill

> 来源：skills/migrate/SKILL.md。旧版 2.x 项目 → 新版 3.0 的一键迁移。

## 流程概览

```text
Step 0: 检测版本 → Step 1: 展示计划+确认 → Step 2: 挪入 old/
→ Step 3: 初始化骨架 → Step 4: 设定迁移（并行 subagent）
→ Step 5: 拷贝正文+提示词 → Step 6: 验收+汇报
```

## 版本检测信号

| 信号 | 结论 |
|------|------|
| `story.yaml` 存在 && `story.md` 不存在 | **v2.x 旧版** → 需要迁移 |
| `story.md` 存在但 `skill_version` < 当前版本 | **待升级迁移** → 需要迁移 |
| 两者都不存在 | **全新项目** → 正常流程 |

## Step 0: 检测

```bash
ls story.yaml story.md 2>/dev/null
```

## Step 1: 展示迁移计划

扫描项目目录，给作者看三张清单：

**文件清单：**
- 设定文件：story.yaml + settings/ 下所有 yaml
- 角色文件：settings/character-setting/ 下所有 yaml
- 卷纲：volumes/ 下所有 yaml
- 正文：archives/ 下 `.md` 文件数量
- 章纲（已归档）：chapters/ 下 `status=archived` 的章节数量
- 章纲（跳过）：chapters/ 下 `status!=archived` 的章节标题和状态
- 提示词：prompts/ 下文件数量

**废弃文件清理（直接丢弃）：**
- `author-intent.md`、`current-focus.md`
- `drafts/`、`drifts/`、`tmp/`、`temp-*.txt`
- `manuscripts/`、`.vscode/`

**作者确认后才继续。**

## Step 2: 整体挪入 old/

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

废弃文件直接删除。不动 `.claude/`、`.deepseek/`、`CLAUDE.md`、`.git/`、`install.sh`、`.gitignore`。

## Step 3: 初始化新骨架

从旧 story.yaml 读取标题和作者，运行 init.py 或手动创建骨架：

```text
story.md + settings/（world/writing/genre/anti-ai/hooks）+ volumes/ + chapters/ + archives/ + prompts/
```

## Step 4: 迁移设定（并行 subagent）

主 agent 启动多个并行 subagent，每个负责一个迁移子步骤。

优先级：characters > chapters > world > writing+genre > anti-ai+hooks > story > volumes

### 4a — story.yaml → story.md

| 输入 | 输出 |
|------|------|
| `old/story.yaml` + `old/volumes/*.yaml` | `story.md` |

关键操作：提取 title/author/created_at → 读各卷 title/core_conflict → 填充引用路径表、故事主线、分卷规划 → 写入 `skill_version: 3.0`

### 4b — world-setting.yaml → settings/world-setting.md

旧 8 个自由文本字段（geography/politics/culture/history/rules/physics/biology/sociology）→ 3 大节（地理/政治/规则）各含子字段。

### 4c — writing-style.yaml + genre-setting

旧版 writing-style 基本 1:1 迁移。旧版 genre_profile 填入选定类型。

### 4d — anti-ai.yaml + hooks.yaml

anti-ai：疲劳词从旧版按类别填入新版分类（副词/动词/形容词/连接词/身体反应）。
hooks：→ 三张摘要表（活跃/已收束/废弃）。

### 4e — 角色 yaml → character-setting/*.md

对 `old/settings/character-setting/` 下每个 yaml 逐一迁移：
- name/story_role/appearance → 直接映射
- background/summary/age/occupation → 背景
- cognition 6 层 → 认知 6 层模型
- relationships → 关系
- state_history → 状态历史
- 旧版无此字段 → 标"待补充"

### 4f — volume yaml → volumes/volume-{N}.md

title → 标题, core_conflict → 核心冲突, chapters_summary → 章节列表

### 4g — chapter yaml → chapter.md（仅 archived）

只处理 `status=archived` 的章节。无数据的字段标"（待补充）"，不捏造。

## Step 5: 拷贝正文 + 提示词

```bash
cp old/archives/*.md archives/
cp old/prompts/*.md prompts/
cp old/prompts/*.txt prompts/ 2>/dev/null
```

正文不做任何修改。不复制 `.draft.md` 文件。

## Step 6: 验收 + 汇报

### 结构验收清单

- [ ] story.md 存在，skill_version = 3.0
- [ ] settings/world-setting.md 存在且已填充
- [ ] settings/writing-style.md 存在且已填充
- [ ] settings/genre-setting.md 存在
- [ ] settings/anti-ai.md 存在
- [ ] settings/foreshadowing.md 存在（hooks 摘要）
- [ ] settings/character-setting/ 每角色一个 .md 文件
- [ ] volumes/ 卷数与旧版一致
- [ ] chapters/ 所有 archived 章节已迁移
- [ ] archives/ 正文全部复制
- [ ] prompts/ 提示词全部复制
- [ ] 旧 .yaml 文件已移入 old/（无残留）
- [ ] 废弃文件已清理

### 汇报格式

```text
迁移完成。
──────────────────────────────
✅ 成功完成（N 项）：
  - story.md → 标题/作者/N卷规划
  - world-setting.md → 已填充
  - 角色 → N 个角色
  - ...

⏭️ 跳过（N 项）：
  - chapters/xxx（status=draft）
  - chapters/xxx（status=outline）

📌 待补充字段：
  - settings/character-setting/*.md → 语言特征、情绪弧线
  - settings/genre-setting.md → 满足类型、节奏规则
──────────────────────────────
old/ 目录保留了所有旧文件，确认无误后可以手动删除。
```
