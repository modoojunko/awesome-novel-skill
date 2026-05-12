# 完整流程走查问题记录

> 2026-05-12 流程走查总结：
> - **P1（崩溃级）**：1 项 — init.py 因缺少模板崩溃
> - **P2（影响一致性和可用性）**：13 项 — 模板格式混乱（YAML vs Markdown混用）、冗余引用、字段名过期、genre-setting.md 未创建、.yaml 残留引用
> - **P3（次要）**：7 项 — status.md 未及时更新、占位符未填充、大文件读取、缺少验收子技能
>
> **最严重问题：** 模板系统格式不统一 —— 4 个模板文件(.md.template)中有 3 个是 YAML 格式，但所有 SKILL 和参考指南要求 Markdown 格式。Agent 读了模板会写错格式。
> **第二大问题：** 职责重叠 —— writing-style.md 的 genre 段 与 genre-setting.md 重复；writing-style.md 臃肿（244行）含 InkOS 方法论参考，实际写作只需要前几段。

## BUG: init.py

- [ ] **P1 init.py 崩溃**: `anti-ai.md.template` 不存在 → init.py 运行到第79行崩溃。创建模板存根后恢复。
- [ ] **P2 genre-setting.md 未创建**: init.py 不生成 `settings/genre-setting.md`，但 Phase 1.2 需要它。
- [ ] **P2 story.md template 残留 `.yaml` 引用**: 第12-13行写 `world-setting.yaml` 和 `writing-style.yaml`，实际文件是 `.md`。
- [ ] **P2 world-setting.md template 标题含 `.yaml`**: 首行 `# world-setting.yaml` 与实际格式不符。
- [ ] **P3 `$NOVEL_SKILL_HOME` 环境变量不存在**: setup SKILL 第24行引用它，但 install.sh 不设置此环境变量。
- [ ] **P3 `{created_at}` 占位符未填充**: story.md 的 `{created_at}` 未像 status.md 那样被 init.py 替换。

- [ ] **P2 writing-style.md 有重复的 genre 段**: 与 genre-setting.md 职责重叠。setup SKILL 说 genre-setting.md 是"独立文件，非 writing-style.md 字段"，但 writing-style.md 模板第 247-270 行也有完整的 genre 配置（type/satisfaction_types/pacing_rules 等）。Agent 不知道该维护哪个。

## 设定阶段的问题

- [ ] **P2 genre-setting.md 创建时机模糊**: setup SKILL 说"先选题材→写作风格确认→类型档案选择→题材配置"，最后写入 genre-setting.md。但题材在"先选题材"步就确认了，创作结果和写入时机不清晰。
- [x] **P2 模板 vs 实际输出格式不一致**: world-setting.md.template 是 YAML-like（冒号值对），但 world-setup-style.md 要求 Markdown `##` 标题。Agent 按模板走会写错格式。
- [ ] **P2 writing-style.md.template 和 anti-ai.md 职责不清**: writing-style.md 有 detailed `possible_mistakes`（20+行）、`depiction_techniques`、`skill_layers`、`creative_constitution` 等，但 anti-ai.md 只存根。这些检测规则应该在哪维护？
- [ ] **P2 writing-style.md 结构臃肿**: 244 行单体文件，混合了 core_principles/possible_mistakes/depiction_techniques 和完整的 InkOS 方法论参考（reader_psychology/desire_engine/immersion_pillars 等应有尽有）。写作者只需前几项。
- [ ] **P2 writing-style.md 的 genre 字段 vs genre-setting.md 冲突**: writing-style.md 已有 `genre` 段（type/satisfaction_types/pacing_rules 共12行），但流程要求写 settings/genre-setting.md。两份数据冗余。
- [ ] **P3 setup 完成后 status.md 不更新**: setup SKILL 说"完成后引导作者进入 outline SKILL"，但没有步骤更新 `current_phase` 从 `setup` 到 `volume`。

## 角色设定问题

- [ ] **P2 init.py 创建 character-setting/template.md**: 这是一个模板参考文件，但 setup 步骤会创建真正的角色文件。模板残留文件不会被清理或提及。

## 主线拆纲+卷纲阶段

- [ ] **P2 volume.md.template 是 YAML 格式**: 模板 `volume.md.template` 是 YAML-like（冒号值对），但 outline SKILL 要求 Markdown 格式（`## 章节列表` + `### N-1` 标题）。
- [ ] **P2 volume-setting-style.md 输出模板格式旧**: 第 327-343 行仍展示 YAML 格式（`title:` / `core_conflict:` / `chapters_summary:`），与 outline SKILL 的 Markdown 格式不一致。
- [ ] **P2 章节列表字段名不一致**: outline SKILL 用 `冲突事件`，volume-setting-style 用 `summary`，实际是同一字段。
- [ ] **P3 status.md 在转换阶段时未更新**: 从 setup 到 volume 到 chapter-loop，没有步骤显式更新 `current_phase`。

## 章节循环阶段

- [ ] **P2 chapter.md.template 是 YAML 格式**: 96 行 YAML-like（`volume: 1` / `memo:` / `payoff_plan:`），但章节设定指南用 Markdown 格式。模板与实际格式不匹配。
- [ ] **P2 prompt.md.template 是填空格式**: 用 `______` 占位，但 prompt SKILL 要求 6 模块自动填充，占位符对生成无用。
- [ ] **P3 chapter-setting-style.md 854 行过长**: 作为参考标准文件太长。chapter SKILL 引它，但一次要读 854 行。
- [ ] **P3 主 SKILL 的"提示词验收"和"正文验收"无子技能**: 这两个验收在主流程 Step 1 提到，但无独立 SKILL.md 或 SOP。Agent 靠记忆执行。
- [ ] **P2 prompt SKILL 引用 "prompt_segment" 字段不存在**: Step 1.4 说"取 prompt_segment"但 genre-example 文件中用中文标题 `提示词注入段`。字段名不一致。
- [ ] **P2 prompt.md.template 与 prompt-setting-style.md 重复**: 两个文件几乎相同（都是 6 模块占位符），模板没有独立存在意义。占用式样不代表实际生成输出。
- [ ] **P3 模板格式不统一**: story.md=Markdown，world-setting.md.template=YAML，volume.md.template=YAML，chapter.md.template=YAML，character.md.template=Markdown。混用两种格式。

## 归档阶段

- [ ] **P2 archive SKILL 第9步"更新 story.md chapters 列表"但 story.md 无此字段**: story.md 有 `分卷规划`，但无逐章列表字段。archive SKILL 引用了一个不存在的列表。
- [ ] **P3 归档后 status.md "current_phase" 未更新**: archive SKILL 更新 status.md，但 current_phase 应改为什么？`chapter-loop`? 归档后回到主流程重新检测——如果所有章都归档了，phase 应变为 `complete`。
- [ ] **P3 主 SKILL 的状态检测依赖文件名解析**: Step 1 说"读 chapters/ 下最大章号的 status"，Agent 需从 `vol-N-ch-M.md` 文件名解析章号。无标准化辅助脚本。
