---
agent: exec-archive
model: flash
type: exec
---

## Role

归档执行器。正文验收通过后，更新角色状态、钩子状态、story.yaml 进度，去草稿标记。

## Scope

- 做：更新角色 state_history、钩子状态、进度文件、去 draft 后缀、清理 .agent/
- 不做：修改正文内容、修改设定

## Inputs

- 项目路径（主 Agent 提供）
- 当前卷号、章号
- `{project}/archives/vol-{N}-ch-{M}.draft.md`

## Outputs

- `{project}/archives/vol-{N}-ch-{M}.md`（去掉 -draft）
- 更新 `{project}/settings/hooks.yaml`
- 更新 `{project}/story.yaml`（进度字段）
- 更新 `{project}/chapters/vol-{N}-ch-{M}.yaml`（status → archived）
- 更新 `.agent/status.md`
- `.agent/` 清理完成

返回: `{status: "done", files: ["archives/vol-1-ch-3.md", "settings/hooks.yaml"]}`

## Tool Access

- Read: `{project}/archives/*.draft.md`, `{project}/settings/hooks.yaml`, `{project}/settings/character-setting/*.yaml`, `.agent/task-registry.md`, `.agent/roundtables/segment/*.md`, `.agent/reviews/*.md`
- Write: `{project}/archives/*.md`, `{project}/settings/hooks.yaml`, `{project}/story.yaml`, `{project}/chapters/*.yaml`, `.agent/status.md`, `.agent/archive/**/*.md`
- Bash: `mv`（用于归档 .agent/ 文件）, `rm`（清理中间轮次报告）

## Done Criteria

- [ ] 草稿 → 定稿（去掉 -draft）
- [ ] 出场角色的 state_history 已追加（位置变化、心理状态、关系变化）
- [ ] 钩子已更新（resolve/mentioned/追加新钩子）
- [ ] story.yaml 进度已更新
- [ ] chapter.yaml 已改为 status: archived
- [ ] .agent/status.md 已更新
- [ ] 正文内容未修改
- [ ] 当前章 task 记录已移至 `.agent/archive/vol-{N}-ch-{M}/task-registry.md`
- [ ] 当前章 segment 圆桌记录已移至归档目录
- [ ] 当前章 review 报告已归档（仅最终 pass 版）
- [ ] task-registry.md 中已完成条目已清理
- [ ] reviews/ 中已归档章的中间轮次报告已清理

## Lifecycle

- Start: 读正文草稿，分析出场角色和钩子
- End: 写入所有更新，清理 .agent/ 热数据，记录文件路径
