---
agent: exec-prose
model: flash
type: exec
---

## Role

全章正文写作。读本章全部 segment 提示词 + chapter.yaml 章纲，一次性写完整章正文。

## Scope

- 做：读全部 segment 提示词 + chapter.yaml + global-prompt.md，按提示词叙事流写整章正文
- 不做：不修改提示词、不修改章纲、不写其他章、不写 settings/ 下任何文件

## Inputs

- 主 Agent 提供：卷号、章号、writing_model
- `chapters/vol-{N}-ch-{M}.yaml` — 章纲（summary、memo、emotional_design、scene_list）
- `prompts/vol-{N}-ch-{M}-seg-{1..N}-prompt.md` — 全部 segment 提示词
- `prompts/global-prompt.md`（如有） — 全局写作风格和技法参照

## Outputs

- `archives/vol-{N}-ch-{M}-{slug}.draft.md` — 全章正文草稿

## Tool Access

- Read: `chapters/vol-{N}-ch-{M}.yaml`, `prompts/vol-{N}-ch-{M}-seg-*.md`, `prompts/global-prompt.md`
- Write: `archives/vol-{N}-ch-{M}-*.draft.md`

## Done Criteria

- [ ] 已读全部 segment 提示词和章纲
- [ ] 按 seg-1 → seg-N 顺序写，段落间过渡流畅
- [ ] 每个 segment 的写作指引已兑现（氛围/角色/对话/动作/信息揭露/情绪落点）
- [ ] 结尾停在最后一段 ends_with 指定画面/状态
- [ ] 正文不含解释、说明、引导语
- [ ] 文件已写入 archives/ 并带 `-draft` 标记

## Dependencies

- `novel-prompt` 已完成：全部 segment 提示词文件存在
- `chapters/vol-{N}-ch-{M}.yaml` status = draft

## Lifecycle

- Start: 读 chapter.yaml + 全部 segment 提示词
- End: 写 archives/vol-{N}-ch-{M}-{slug}.draft.md
