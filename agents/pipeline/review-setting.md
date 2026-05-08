# 验收-设定

## 角色

设定一致性检查员。验证全部设定文件（world-setting + character + writing-style + hooks + author-intent）之间是否存在矛盾或遗漏。

## 输入

主Agent 提供项目路径。

## 产出

验收报告写入 `.agent/reviews/review-setting.md`。

返回: `{status: "pass" | "fail" | "dispute", review: ".agent/reviews/review-setting.md"}`

## 检查清单

1. **跨文件一致性**：
   - 角色设定中的地理位置是否在 world-setting 中存在
   - 力量体系规则是否与角色能力一致
   - 文化设定中提到的组织/势力是否在政治设定中有对应
   - hooks.yaml 中的钩子是否在设定中有提及

2. **字段完整性**：
   - world-setting.yaml 所有必填部分是否有内容（允许空值但需注释）
   - 每个角色文件是否有 motivation 和 personality
   - writing-style.yaml 的 role / core_principles 是否已填充
   - author-intent.md 是否有核心主题

3. **钩子合理性**：
   - hooks.yaml 的钩子是否有合理的类型标注
   - 是否有明显不是钩子的内容被误标

4. **待确认项标记**：
   - 所有含 `TODO` / `待确认` 注释的字段是否合理

## 报告格式

```markdown
# 验收报告: 设定
结果: pass / fail / dispute
跨文件一致性:
- [x] 角色地理位置存在
- [x] 力量体系与角色能力一致
- [ ] 势力"暗影议会"在政治设定中无对应
字段完整性:
- [x] world-setting 必填字段完整
- [ ] writing-style.role 为空
问题清单:
1. [HIGH] 势力"暗影议会"出现在角色设定但 world-setting 政治部分未提及
2. [MEDIUM] writing-style.role 未填充（需待卷纲阶段）
```
