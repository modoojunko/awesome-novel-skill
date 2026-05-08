# Harness 审计 — 流程走查问题清单

## 一、缺失的 Agent

### 1.1 缺少 exec-volume
Step 3.1 完成后的产物是 `volume.yaml`，但没有 agent 负责写入它。
- 5 个圆桌 agent 各出一版方案 → 圆桌收敛 → 但谁写 volume.yaml？
- 需要新增 `exec-volume`（或由 exec-outline 兼任，但职责不同）

### 1.2 缺少 exec-segment
Step 3.3 的圆桌方案存在 5 份分散的 segment 记录，但没有人把它们写进 `chapter.yaml` 的 `segments` 字段。
- exec-prompt 的 Inputs 写着"段拆分方案文件"，但不存在单一文件
- 需要新增 `exec-segment`，从 5 份 segment 圆桌记录提炼出每章的段拆分方案，写入 chapter.yaml

### 1.3 缺少 review-outline
Step 3.2 exec-outline 写完 chapter.yaml 后，没有 review agent 检查章纲质量。
- 如果 chapter.yaml 有错误（如钩子操作不合理、情绪曲线与剧情矛盾），直到 Step 4 review-prompt 才会被发现
- 需要新增 `review-outline`，检查 chapter.yaml 与 volume.yaml 的一致性

---

## 二、流程定义缺失

### 2.1 圆桌收敛机制未定义
SKILL.md 说"圆桌收敛"但没有定义主 Agent 怎么执行收敛。
- 当前设计：5 个 agent 各自写方案到文件，主 agent 只转发不读内容
- 但收敛需要：主 agent 读出各 agent 方案中的矛盾点 → 分别发给对应的 agent → 让它们调整
- 矛盾点谁来找？如果主 agent 不读内容，需要另一个角色来找矛盾

**根本问题**：圆桌阶段的收敛协议没定义。

### 2.2 exec-agent 的依赖顺序未定义
exec-world → exec-character（角色需要知道世界地理）
exec-character → exec-style（风格与角色相关）
这四个完成后才能 exec-meeting-notes（需要所有设定）

但 agent .md 中没有定义这些依赖关系。主 agent 派活时不知道谁必须先跑。

### 2.3 exec-prose 并行派发未定义
SKILL.md 写 "exec-prose(并行)" 但主 agent 的派活机制没有定义并行逻辑。
- 是同一个 agent 派 N 次（N=段数）？
- 还是每次派活指定不同的 seg 参数？
- task registry 怎么写 N 个 task？

### 2.4 exec-de-ai 在 review 循环中的位置不对
当前流程：prose → stitch → de-ai → review
如果 review fail 丢回 exec-prose 修，修完应该：prose(修) → stitch → de-ai → review
但路由规则只说"丢回原执行修"，没说重跑 stitch 和 de-ai。

---

## 三、文件格式/路径不一致

### 3.1 exec-prompt 的输入来源不明确
Inputs 写"段拆分方案文件"但没有给出具体路径。
- 需要段方案文件的路径约定（如 `.agent/roundtables/segment/` 下的哪几个文件）
- 或者等 exec-segment 产出 consolidated 文件后再读

### 3.2 exec-stitch 不知道段数量
"本章所有 segment 草稿路径列表"——主 agent 传这个列表？还是 agent 自己去目录发现？
- 如果主 agent 传，它需要知道段数
- 如果 agent 自己发现，需要约定文件命名模式

### 3.3 .agent/ 子目录未在 init 中创建
exec-init 创建 `.agent/status.md` 但没创建：
- `.agent/roundtables/setting/`
- `.agent/roundtables/volume/`
- `.agent/roundtables/chapter/`
- `.agent/roundtables/segment/`
- `.agent/reviews/`
- `.agent/lessons/`
- `.agent/archive/`

后面步骤的 agent 假设这些目录存在，但没人创建。

---

## 四、圆桌 Agent 的 Done Criteria 不可机械判断

所有 15 个圆桌 agent 的 Done Criteria 都是"连续 3 回合作者没有新信息补充"。

但主 agent 是转述者——它需要问 agent "你还有问题吗？"，agent 说"没有了"才算停。目前的格式只定义了 agent 和作者之间的停止条件，没定义 agent 和主 agent 之间的停止信号。

需要加一条：当主 agent 问"还有问题吗？"时，agent 明确回答"没有"才算 done。

---

## 问题严重度分级

| # | 问题 | 严重度 | 影响 |
|---|------|--------|------|
| 1.1 | 缺少 exec-volume | HIGH | 3.1 完成后 volume.yaml 没人写 |
| 1.2 | 缺少 exec-segment | HIGH | 3.3 完成后段方案没落盘，后续无法用 |
| 1.3 | 缺少 review-outline | MEDIUM | 章纲错误延期到 Step 4 才发现 |
| 2.1 | 圆桌收敛协议未定义 | HIGH | 圆桌阶段无法自动完成收敛 |
| 2.2 | exec 依赖顺序未定义 | MEDIUM | 主 agent 可能顺序错误 |
| 2.3 | 并行派发未定义 | MEDIUM | exec-prose 并行实现不确定 |
| 2.4 | de-ai 在 review 循环中的位置 | LOW | 增加了无用轮次但功能正确 |
| 3.3 | .agent/ 子目录未创建 | MEDIUM | 后面步骤写文件会失败 |
| 4 | 圆桌停止信号不明确 | LOW | 多问一轮可以绕过 |
