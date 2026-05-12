---
name: novel-prompt-verify
description: 提示词验收——检查生成的 prompt.md 是否完整、可执行。触发：主流程检测到 outline + prompt 文件存在时自动分发。
---

# Novel Prompt Verify — 提示词验收

> 读 `references/prompt-setting-style.md` Section 三，逐条检查。展示报告给作者确认。

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
4. **通过** → 更新 `chapters/vol-{N}-ch-{M}.md` status 为 `draft`
5. **不通过** → 返回 `skills/prompt/SKILL.md` 修改

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
