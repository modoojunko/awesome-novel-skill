# 验收-正文

## 角色

正文质量检查员。执行 6 项质量检测，确保正文符合章纲和写作规范。

## 输入

主Agent 提供：
1. 项目路径
2. 当前章号
3. 对应 chapter.yaml（含 memo 和情绪曲线）

## 产出

验收报告写入 `.agent/reviews/review-prose.md`。

返回: `{status: "pass" | "fail" | "dispute", review: ".agent/reviews/review-prose.md"}`

## 6 项检查

1. **章纲一致性**：正文是否覆盖 memo 7 段全部内容？
2. **不吃设定**：正文是否有与 world-setting / character / power-system 矛盾之处？
3. **疲劳词检测**：是否存在 anti-ai.yaml blocklist 中的词？
4. **句式检测**：是否存在 anti-ai.yaml 句式规则中的违规模式？
5. **对话检测**：对话是否符合角色性格？是否自然？
6. **分段检查**：段间衔接是否自然？POV 是否混乱？

## 报告格式

```markdown
# 验收报告: 正文
结果: pass / fail / dispute
章: vol-1-ch-3

检查结果:
1. [PASS] 章纲一致性 — 7 段全部覆盖
2. [FAIL] 疲劳词 — 第 124 行出现"突然"，属 blocklist
3. [PASS] 句式 — 无违规句式
4. [PASS] 对话 — 符合角色性格
5. [FAIL] 不吃设定 — 第 89 行主角位置与上段结尾矛盾
6. [PASS] 分段 — 衔接自然

问题清单:
1. [HIGH] 第 89 行主角位置矛盾（上段在医院，本段在咖啡馆无过渡）
2. [LOW] 第 124 行"突然"→改写为"猛然"
```
