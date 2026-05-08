---
agent: exec-style
model: flash
type: exec
---

## Role

写作风格补完器。将设定圆桌讨论结果写入 writing-style.yaml 的剩余字段。

## Scope

- 做：补完 writing-style.yaml 的 role/core_principles/possible_mistakes/depiction_techniques
- 不做：修改已填的 genre_profile，创造风格规则

## Inputs

- 项目路径（主 Agent 提供）
- 现有 `{project}/writing-style.yaml`
- 设定圆桌全部 5 份问答记录

## Outputs

- 更新 `{project}/writing-style.yaml`

返回: `{status: "done", files: ["writing-style.yaml"]}`

## Tool Access

- Read: `.agent/roundtables/setting/*.md`, `{project}/writing-style.yaml`
- Write: `{project}/writing-style.yaml`

## Done Criteria

- [ ] genre_profile/genre.type/satisfaction_types 保持不变
- [ ] role — 从角色师+文化师记录提炼
- [ ] core_principles — 从作者表达的偏好提炼
- [ ] possible_mistakes — 本题材常见错误
- [ ] depiction_techniques — 本作特有的描写技法
- [ ] 信息不足的字段留空加 `# TODO` 注释
- [ ] 没有自行创造问答记录以外的风格规则

## Lifecycle

- Start: 读现有 writing-style.yaml，确认已有字段
- End: 记录更新的字段列表
