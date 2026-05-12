# Awesome Novel 精简 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 移除 awesome-novel 中 complexity/ROI 倒挂的 4 个组件——genre-corpus 继承体系、anti-ai 规则引擎、Phase 4 独立入口、install.sh 冗余拷贝。

**Architecture:** 不动核心领域模型（story.yaml/hooks.yaml/6 phase 框架/正文质量检查），只删 infra 代码和合并入口。改动集中在 `genre-corpus/`、`scripts/`、`skills/review/`、`SKILL.md`。

**Tech Stack:** YAML / Markdown / Python / Shell

---

### Task 1: Genre corpus 扁平化——variant 移到根目录

**Files:**
- Modify: `genre-corpus/index.yaml` — 删除 variant 查找逻辑的注释
- Modify: 14 variant files — 从 `genre-corpus/variant/` 移到 `genre-corpus/`
- Delete: `genre-corpus/variant/` 目录
- Verify: 确认每个 variant 文件已自包含

- [ ] **Step 1: 将 14 个 variant 文件移到 genre-corpus/ 根目录**

```bash
# 从 variant/ 移到根目录，保持文件名不变
mv /home/zhuke/awesome-novel-skilll/genre-corpus/variant/*.yaml /home/zhuke/awesome-novel-skilll/genre-corpus/
```

预期结果：`ls genre-corpus/*.yaml` 显示 24 个 YAML 文件，无 variant/ 子目录。

- [ ] **Step 2: 更新 index.yaml——删除 variant 查找逻辑注释**

当前 index.yaml 第 3 行有 `Phase 4 读取时：先读 corpus 指向的基类，再叠加 variant/ 同名文件的差异字段`。扁平化后不需要 variant 叠加逻辑，都是自包含文件。

修改 `genre-corpus/index.yaml` 头部注释：

```yaml
# index.yaml — 24种分类注册表
# 每个条目指向一个自包含的 corpus 文件（不再分层叠加）
```

不需要改 genres 列表本身（`corpus:` 字段仍指向文件名，现在所有文件在同一个目录，路径不变）。

- [ ] **Step 3: 验证——确认 install.sh 不需改（已用 `-r` 递归拷贝整个目录）**

```bash
# install.sh 第 72 行是 cp -r "$SCRIPT_DIR/genre-corpus" "$DEST/"
# 删掉 variant/ 后 -r 递归拷贝少一个子目录，行为正确
# 验证安装后文件结构：
ls /tmp/genre-corpus-test/*.yaml | wc -l  # 应 = 24
```

- [ ] **Step 4: 确认 prompt/SKILL.md 中 variant 路径引用不需要改**

prompt/SKILL.md 第 170 行：`读 variant/{genre_profile}.yaml（若存在）`——variant 移到根目录后，相对路径不再需要 variant/ 前缀。但 prompt/SKILL.md 本身的内容会被 Task 3 处理。

暂不做修改，留到 Task 3 一并处理。

- [ ] **Step 5: 确认 style-extract 技能无 variant 引用**

```bash
grep -rn 'variant/' /home/zhuke/awesome-novel-skilll/skills/style-extract/ 2>/dev/null || echo "no references"
```

无引用 → 无需修改。

---

### Task 2: 删除 anti-ai.yaml.template 和 analyze_style.py

**Files:**
- Delete: `scripts/templates/anti-ai.yaml.template`
- Delete: `scripts/analyze_style.py`
- Modify: `skills/review/SKILL.md` — 在适当地点加 AI 味手检 checklist
- Modify: `SKILL.md` — 删除 Bundled Resources 中对这两个文件的引用

- [ ] **Step 1: 删除 anti-ai.yaml.template**

```bash
rm /home/zhuke/awesome-novel-skilll/scripts/templates/anti-ai.yaml.template
```

命令不含输出。文件不存在时 rm 会报错——确认路径正确。

- [ ] **Step 2: 删除 analyze_style.py**

```bash
rm /home/zhuke/awesome-novel-skilll/scripts/analyze_style.py
```

- [ ] **Step 3: 更新 SKILL.md——删除 Bundled Resources 中 analyze_style.py 的引用**

当前 SKILL.md 第 134 行：
```markdown
| `scripts/analyze_style.py` | 参考小说文风统计分析（12 项量化指标） | novel-style-extract Step 1 时执行 |
```

改为：
```markdown
<!-- 原 analyze_style.py 引用已删除，AI 味检测移至 review 技能自检清单 -->
```

或者直接删除整行。删掉更干净。

Edit SKILL.md line 134-135:
```
| `scripts/analyze_style.py` | 参考小说文风统计分析（12 项量化指标） | novel-style-extract Step 1 时执行 |
```

整行删除。

- [ ] **Step 4: 更新 SKILL.md——删除 Bundled Resources 中 anti-ai.yaml.template 的引用（若有）**

确认 SKILL.md 中是否有引用 `anti-ai.yaml`——从 grep 结果看没有。跳过此步。

- [ ] **Step 5: 更新 review/SKILL.md——在 Step 2 上下文收集列表中移除 anti-ai.yaml 引用**

当前 review/SKILL.md 第 53 行：
```markdown
| `settings/anti-ai.yaml` | AI 味规则——fatigue_words、sentence_rules、paragraph_rules、dialogue_rules（评审时参考，不重复 Phase 5 检查） |
```

改为：
```markdown
| `settings/anti-ai.yaml`（若存在） | 原有 AI 味规则（评审时参考，不重复 Phase 5 检查）。新项目不再生成此文件——AI 味检测由下方 checklist 执行 |
```

- [ ] **Step 6: 更新 review/SKILL.md——在评审维度后或 Step 4 前加 AI 味手检 checklist**

在 review/SKILL.md 的 Step 3 "评审维度与细项" 之后、Step 4 "呈现报告" 之前，插入 AI 味自检 checklist。

在 "维度 10：逻辑与内部一致性" 之后插入：

```markdown
### AI 味手检（读完本章后逐项过）

> 替代原有的 anti-ai.yaml 规则引擎。不阻断评审流程——作为补充信息附在报告末尾。

| # | 检查项 | 检查方法 | 判定 |
|---|--------|---------|------|
| AI.1 | 「了」字病 | 每段不超过 2 个「了」。随机抽 3 个段落计数 | ✅/⚠️/❌ |
| AI.2 | 感知词模板 | 全文「感到/看到/听到/闻到/想到」超过 3 处 | ✅/⚠️/❌ |
| AI.3 | 「不是……而是……」句式 | 全文超过 1 处 | ✅/⚠️/❌ |
| AI.4 | 身体部位+情绪模板 | 「心头一紧」「嘴角上扬」「眼眶一热」等超过 2 处 | ✅/⚠️/❌ |
| AI.5 | 副词密度 | 每 100 字超过 3 个「地」 | ✅/⚠️/❌ |
| AI.6 | 对话占比 | 对话占正文比例低于 20% | ✅/⚠️/❌ |

**输出格式**（追加到评审报告末尾）：

```
### AI 味手检结果

| # | 检查项 | 结果 | 说明 |
|---|--------|------|------|
| AI.1 | 「了」字病 | ❌ | 第 2 段出现 4 个「了」 |
| AI.2 | 感知词模板 | ✅ | 仅 1 处「感到」 |
| AI.3 | 「不是……而是……」 | ✅ | 0 处 |
| AI.4 | 身体部位+情绪模板 | ⚠️ | 1 处「眼眶一热」 |
| AI.5 | 副词密度 | ✅ | 约 1.5 个/百字 |
| AI.6 | 对话占比 | ✅ | 约 35% |
```
```

具体插入位置：在 `### 维度 10：逻辑与内部一致性` 的表格之后、`---` 评分标准之前。找 review/SKILL.md 第 232 行的 `## 评分标准` 之前插入。

- [ ] **Step 7: 确认 install.sh 不拷贝这两个文件（install.sh 用目录级别拷贝，已删除的文件不会被拷贝）**

```bash
# install.sh: cp -r "$SCRIPT_DIR/scripts" "$DEST/" — 整个 scripts/ 目录递归
# 删除 scripts/templates/anti-ai.yaml.template 后，拷贝时消失
# 删除 scripts/analyze_style.py 后，拷贝时消失
# 不需要改 install.sh 的拷贝命令
```

---

### Task 3: Phase 4 合并——删除独立路由，保留参考文档

**Files:**
- Modify: `SKILL.md` — 删除 Phase 4 路由、更新分发表、模型门禁
- Modify: `skils/outline/SKILL.md` — 更新 auto-generation 部分 self-contained，删除 Read prompt skill 引用
- Keep: `skills/prompt/SKILL.md` — 保留为参考文档（outline skill 仍可读取），但不作为独立 sub-skill 入口
- Modify: `install.sh` — 从拷贝列表中删除 `skills/prompt/`

- [ ] **Step 1: 更新 SKILL.md——用户意图匹配表**

删除第 62 行：
```
| "生成提示词""视角转换" | Phase 4 | `novel-prompt` |
```

改为：
```
| "生成提示词""视角转换" | Phase 3 自动生成 | → 路由到 `novel-outline`，提示词在章纲确认后自动组装，可直接手动调整 prompt 文件 |
```

- [ ] **Step 2: 更新 SKILL.md——Step 3 跳 Phase 检测**

第 72 行：
```
- 目标 Phase 4 → 已移入 Phase 3 自动执行。手动进入 Phase 4（`novel-prompt`）时检查 memo 是否完整
```

改为：
```
- 目标 Phase 4 → 已合并到 Phase 3。章纲确认后自动执行提示词生成。手动调整提示词直接编辑 `prompts/` 下的文件
```

- [ ] **Step 3: 更新 SKILL.md——Step 5 分发表**

第 91 行：
```
| Phase 4（手动） | novel-prompt — 手动调整提示词。正常流程已在章纲确认后自动执行 | `skills/prompt/SKILL.md` |
```

改为：
```
| Phase 4（参考） | novel-prompt（已合并到 Phase 3）。章纲确认后自动生成提示词；手动调整直接编辑 prompt 文件 | 不再独立路由。自动执行见 `skills/outline/SKILL.md` 末尾「章纲确认后自动生成提示词」 |
```

或直接删除该行——Phase 4 不再作为可分发入口。

- [ ] **Step 4: 更新 SKILL.md——模型门禁表**

第 111 行：
```
| 4 | novel-prompt | **sonnet（强制）** | 视角转换、segment 拆分、提示词组装——最耗推理 |
```

改为：
```
| 4 | novel-prompt（已合并到 Phase 3） | **sonnet（强制）** | 视角转换、segment 拆分、提示词组装——最耗推理。自动执行，由 outline 技能承载 |
```

- [ ] **Step 5: 更新 outline/SKILL.md——auto-generation 部分不再引用 prompt/SKILL.md**

outline/SKILL.md 第 280 行：
```
1. Read `skills/prompt/SKILL.md`，获取以下规则的具体内容：
```

改为自包含引用（不要求读取外部文件）：
```
1. 按以下规则执行（规则来自 `skills/prompt/SKILL.md`，已内联至此）：
```

第 316 行：
```
- "我自己调" → 主 Agent Read `skills/prompt/SKILL.md` 进入 Phase 4（手动模式）
```

改为：
```
- "我自己调" → 直接编辑 `prompts/vol-{N}-ch-{M}-prompt.md` 文件，或参考 `skills/prompt/SKILL.md` 中的规则手动调整
```

- [ ] **Step 6: 更新 outline/SKILL.md——anti-ai.yaml 引用**

第 290 行：
```
c. 读 writing-style.yaml / anti-ai.yaml / genre-corpus / world-setting / archives
```

改为：
```
c. 读 writing-style.yaml / genre-corpus / world-setting / archives
（anti-ai.yaml 已废弃，AI 味检测移至 review 技能的自检 checklist）
```

- [ ] **Step 7: 更新 SKILL.md——Bundled Resources 中 genre-corpus 和 analyze_style 引用**

第 134-136 行：
```markdown
| `scripts/analyze_style.py` | 参考小说文风统计分析（12 项量化指标） | novel-style-extract Step 1 时执行 |
...
| `genre-corpus/` | 类型档案（24 种预置类型，7 个基类 + 变体覆盖） | Phase 2 设定阶段选择类型档案；Phase 4 提示词注入 prompt_segment |
```

改为：
```markdown
| `genre-corpus/` | 类型档案（24 种预置类型，自包含文件） | Phase 2 设定阶段选择类型档案；Phase 3 提示词注入 prompt_segment |
```

- [ ] **Step 8: 删除 prompt/SKILL.md 中的 variant/ 路径引用（继承 Task 1 的文件移动）**

prompt/SKILL.md 第 170 行：
```markdown
[在 index.yaml 的 genres 列表中查找 genre_profile 的 corpus 字段 → 读 genre-corpus/{corpus} 的 role_override.role + role_override.personality]
[然后读 variant/{genre_profile}.yaml（若存在），合并覆盖]
```

改为：
```markdown
[在 index.yaml 的 genres 列表中查找 genre_profile 的 corpus 字段 → 读 genre-corpus/{corpus} 的 role_override.role + role_override.personality]
[再读 genre-corpus/{genre_profile}.yaml（若存在），合并覆盖（variant 文件已扁平化到 genre-corpus/ 根目录）]
```

第 179 行：
```markdown
[在 index.yaml 中查找 genre_profile 的 corpus → 读 genre-corpus/{corpus} 的 prompt_segment]
[再读 variant/{genre_profile}.yaml（若存在），合并差异]
```

改为：
```markdown
[在 index.yaml 中查找 genre_profile 的 corpus → 读 genre-corpus/{corpus} 的 prompt_segment]
[再读 genre-corpus/{genre_profile}.yaml（若存在），合并差异]
```

第 363 行：
```markdown
- 检查 `~/.claude/skills/awesome-novel/genre-corpus/variant/{genre_profile}.yaml` 是否存在：存在则读取，覆盖/追加差异字段。
```

改为：
```markdown
- 检查 `~/.claude/skills/awesome-novel/genre-corpus/{genre_profile}.yaml` 是否存在：存在则读取，覆盖/追加差异字段（variant 文件已扁平化到根目录）。
```

- [ ] **Step 9: 更新 outline/SKILL.md genre-corpus 路径引用（同上 variant 扁平化）**

确认 outline/SKILL.md 中是否有 variant 路径引用：
```bash
grep -n 'variant/' /home/zhuke/awesome-novel-skilll/skills/outline/SKILL.md
```

有则改。从 grep 结果看 outline/SKILL.md 没有 variant 路径引用——跳过。

- [ ] **Step 10: 更新 install.sh——从拷贝列表移除 skills/prompt/**

install.sh 第 71 行：
```bash
cp -r "$SCRIPT_DIR/skills" "$DEST/"
```

skills/prompt 是 skills/ 的子目录。有两种选择：
A) 保留 `cp -r skills` 整目录拷贝——不再拷贝 prompt 目录（需要额外处理）
B) 改为逐层拷贝，排除 prompt

更简单的方式：**不修改 install.sh 的 skills 拷贝命令**。prompt/SKILL.md 保留在磁盘上作为参考文档，即使被拷贝到安装目录也不影响功能——SKILL.md 路由表已不再分发到它。这符合 YAGNI——不为了"干净"增加维护成本。

**决定：不动 install.sh 的 skills 拷贝命令。prompt/SKILL.md 退化为参考文档，安装后仍存在但不被路由。**

---

### Task 4: 最终验收

- [ ] **Step 1: 确认所有改动后的 SKILL.md 路由表一致**

```bash
# 检查 SKILL.md 中 Phase 4 相关引用已全部更新
grep -n 'Phase 4\|novel-prompt\|analyze_style' /home/zhuke/awesome-novel-skilll/SKILL.md
```

预期输出：只剩"已合并到 Phase 3"或类似注释，无独立入口。

- [ ] **Step 2: 确认 review/SKILL.md 中 anti-ai.yaml 引用已更新，AI 味 checklist 已插入**

检查 review/SKILL.md 中是否存在 "AI 味手检" 标题，确认 anti-ai.yaml 的描述改为"若存在"。

- [ ] **Step 3: 确认 genre-corpus/ 无 variant/ 目录**

```bash
ls /home/zhuke/awesome-novel-skilll/genre-corpus/variant/ 2>&1
# 预期：No such file or directory
```

- [ ] **Step 4: 确认 scripts/templates/anti-ai.yaml.template 和 scripts/analyze_style.py 已删除**

```bash
ls /home/zhuke/awesome-novel-skilll/scripts/templates/anti-ai.yaml.template 2>&1
ls /home/zhuke/awesome-novel-skilll/scripts/analyze_style.py 2>&1
# 预期：No such file or directory
```

- [ ] **Step 5: 确认 outline/SKILL.md 不再说 "Read `skills/prompt/SKILL.md`"**

```bash
grep -n 'Read.*prompt' /home/zhuke/awesome-novel-skilll/skills/outline/SKILL.md
```

预期：无匹配或只有注释性引用。

- [ ] **Step 6: 确认 install.sh 可正常运行**

```bash
# 安装到临时目录做验证
bash /home/zhuke/awesome-novel-skilll/install.sh claude-code 2>&1 | tail -3
# 预期：安装完成
```
