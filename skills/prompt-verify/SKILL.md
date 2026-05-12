---
name: novel-prompt-verify
description: 提示词验收——检查生成的 prompt.md 是否完整、可执行。触发：主流程检测到 outline + prompt 文件存在时自动分发。
---

# Novel Prompt Verify — 提示词验收

> 读 `references/prompt-setting-style.md` Section 三，逐条检查。展示报告给作者确认。

## 工具契约

| 工具 | 用途 | 限制 |
|------|------|------|
| Read | 读 prompt.md、chapter.md 章纲、references/prompt-setting-style.md | — |
| Write/Edit | 更新 chapter.md status → draft（通过时） | 不改 prompt.md 本身 |

## 错误恢复

| 失败场景 | 恢复策略 |
|---------|---------|
| prompt.md 格式异常（6 模块不完整） | 列出缺失模块，返回 prompt SKILL 补全，不写入 status |
| 章纲与 prompt 不一致 | 标记具体偏差项，返回 prompt SKILL 修正，不自行修改 |

## 执行前提

| 检查项 | 操作 |
|--------|------|
| prompt.md 存在 | `prompts/vol-{N}-ch-{M}-prompt.md` 不存在 → **STOP** |
| 章纲完整 | `chapters/vol-{N}-ch-{M}.md` 的 memo 和 emotional_design 非空 |

## 验收步骤

1. 读 `references/prompt-setting-style.md` Section 三（验收标准）
2. 逐条检查 prompt.md：
   - 6 模块是否完整（定位/承接/人物/叙事任务/文字要求/真人感）
   - 每模块字段是否填充（无 `______` 占位符残留）
   - writing-style 四字段是否注入（core_principles / possible_mistakes / depiction_techniques / workflow）
   - 字数目标和叙事视角是否明确
3. 展示验收报告给作者确认
4. **[Checkpoint]** **通过** → 更新 `chapters/vol-{N}-ch-{M}.md` status 为 `draft`
5. **[Checkpoint]** **不通过** → 返回 `skills/prompt/SKILL.md` 修改

## 验收报告格式

```markdown
## 提示词验收报告：第 {N} 章
✅ 通过 / ❌ 需修改

| 检查项 | 结果 | 说明 |
|--------|------|------|
| 6 模块完整 | ✅/❌ | |
| 字段填充完整 | ✅/❌ | |
| writing-style 注入 | ✅/❌ | |
| 字数目标明确 | ✅/❌ | |
| 叙事视角锁定 | ✅/❌ | |

### 问题项
...
```
