# 验收章纲 skill

章纲产出后，逐项检查质量和完整性。全部通过才进入提示词生成阶段。验收标准参考 `.claude/knowledge/chapter-setting-style.md`。

## 流程

结构化反馈（给作者看）→ 检查清单自检 → 快速嗅探 → AI 味自检

## 一、给作者看结构化反馈

按 `chapter-setting-style.md` 做完之后——验收流程 §第 1 步 的格式展示给作者。作者明确说"对"才算通过。"差不多""你看着写"不算。

未通过 → 回到 STEP 3 修改。

## 二、检查清单自检

按 `chapter-setting-style.md` 做完之后——验收流程 §第 2 步 的 24 项清单逐项核实。一项不合格就退回修改。

## 三、快速嗅探

按 `chapter-setting-style.md` 做完之后——验收流程 §第 3 步 执行。

## 四、AI 味自检与去除

按 `chapter-setting-style.md` 风骨层的"6种要命模式"和"空洞形容词速查"扫描全文。命中任一条 → 修改后重新检查，确认全部清除才算通过。

## 五、确认

全部检查通过后，写入 `chapters/vol-{N}-ch-{M}.md`，status → `outline`
