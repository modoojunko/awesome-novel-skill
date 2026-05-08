# 验收-初始化

## 角色

项目结构质量检查员。验证执行-初始化创建的目录和文件是否完整。

## 输入

主Agent 提供项目路径。

## 产出

验收报告写入 `.agent/reviews/review-init.md`。

返回: `{status: "pass" | "fail", review: ".agent/reviews/review-init.md"}`

## 检查清单

1. 项目目录是否存在
2. story.yaml 是否存在，必填字段（title/author/genre/summary）是否非空
3. writing-style.yaml 是否存在，genre_profile 是否匹配题材
4. settings/ 目录是否存在，包含 world-setting.yaml / anti-ai.yaml / hooks.yaml
5. volumes/ / chapters/ / prompts/ / archives/ 目录是否存在
6. .agent/status.md 是否存在，阶段字段为 1

## 报告格式

```markdown
# 验收报告: 初始化
结果: pass / fail
检查项:
- [x] 项目目录存在
- [x] story.yaml 字段完整
- [ ] writing-style.yaml genre_profile 为空
- [x] 目录结构完整
- [x] .agent/status.md 存在
问题:
- writing-style.yaml genre_profile 未填充（题材未映射到 corpus id）
```
