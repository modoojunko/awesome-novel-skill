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
| prompt.md 格式异常（9 层不完整） | 列出缺失层级，返回 prompt SKILL 补全，不写入 status |
| 章纲与 prompt 不一致 | 标记具体偏差项，返回 prompt SKILL 修正，不自行修改 |

## 执行前提

| 检查项 | 操作 |
|--------|------|
| prompt.md 存在 | `prompts/vol-{N}-ch-{M}-prompt.md` 不存在 → **STOP** |
| 章纲完整 | `chapters/vol-{N}-ch-{M}.md` 的 memo 和 emotional_design 非空 |

## 验收步骤

1. 读 `references/prompt-setting-style.md` Section 三（验收标准）
2. 逐条检查 prompt.md：
   - 9 层是否完整（L1-L9）
   - 每层字段是否填充（无 `______` 占位符残留）
   - writing-style 四字段是否注入
   - 字数目标和叙事视角是否明确（L1）
   - 防AI味约束是否注入（L8 含 anti-ai 来源标注 + L9 含质感字段）
   - 冲突检测：L2=L4 起点、L4 落点=L5 拐点、L7 释放位置在 L5 中存在
3. 展示验收报告给作者确认
## 下一步

**状态汇报 + 自动路由：**
- ✅ 提示词验收通过：`chapters/vol-{N}-ch-{M}.md` → `status: draft`
- 📄 提示词已验证：`prompts/vol-{N}-ch-{M}-prompt.md`
- → 主流程检测到 `status=draft` + 无 draft 文件，**分发到正文写作**（`skills/write/SKILL.md`）

**不通过时：** 返回 `skills/prompt/SKILL.md` 修改提示词。

---

**作者选择：**
- 确认通过后 → 主流程分发到正文写作
- 要求修改 → 返回提示词生成

## 验收报告格式

```markdown
## 提示词验收报告：第 {N} 章
✅ 通过 / ❌ 需修改

| 检查项 | 结果 | 说明 |
|--------|------|------|
| 9 层完整 | ✅/❌ | |
| 字段填充完整 | ✅/❌ | |
| writing-style 注入 | ✅/❌ | |
| L2 来龙画面感 | ✅/❌ | |
| L5 场景种子叙事性 | ✅/❌ | |
| L6 约束双侧闭合 | ✅/❌ | |
| L7 爽点释放具体 | ✅/❌ | |
| L8 来源标注 | ✅/❌ | |
| L9 质感字段 | ✅/❌ | |

### 问题项
...
```
