# Awesome Novel 精简设计

## 动机

学习 web-video-presentation 技能后，发现 awesome-novel 在 4 个点上
complexity/ROI 倒挂。本设计针对这 4 点做减法，不动核心领域模型
（story.yaml / hooks.yaml / 6 阶段框架 / 正文质量检查）。

## 范围

| 做 | 不做 |
|---|------|
| genre-corpus 继承体系 → 自包含文件 | story.yaml 字段 |
| anti-ai.yaml + analyze_style.py → reviewer checklist | hooks.yaml 追踪模型 |
| Phase 4 合并到 Phase 3 | writing-style.yaml 四个字段 |
| 删 skills/prompt/ 子技能 | 15 项质量检查清单 |
| | 6 phase 大框架 |
| | skills/write/、archive/、review/ |

---

## 1. Genre corpus 扁平化

### 现状问题

`genre-corpus/` 有 12 个语料文件 + 14 个 variant 覆盖文件 + index.yaml
注册表。读取一个语料需要：查 index.yaml → 确定基类 → 读基类文件 →
读 variant 覆盖 → 合并。这是编译器前端的设计模式，不是写作工具需要的。

### 改动

每个 genre 一个自包含 YAML 文件，放在 `genre-corpus/flat/` 目录：

```
genre-corpus/
├── flat/
│   ├── xianxia.yaml
│   ├── urban.yaml
│   ├── urban-brained.yaml
│   ├── urban-daily.yaml
│   └── ...  # 所有 genre 平铺，不再分层
└── index.yaml  # 保留，只做注册表（id → 文件名映射）
```

variant 和基类的重复量很小（约 20%），重复的代价远低于继承系统的
认知税。

### 影响范围

- 删除 `genre-corpus/variant/` 目录
- 删除 index.yaml 中的 base/variant 继承逻辑（如果有的话）
- 合并每个基类+变体为一个文件
- 涉及文件：~26 个 → ~20 个

---

## 2. 反 AI 味检测简化

### 现状问题

两层代码 703 行：
- `anti-ai.yaml.template`（284 行）：blocklist（副词/动词/形容词/连接词/
  身体反应分类）+ 句式规则（"不是而是"等 8 种 pattern）+ 改写算法
  （感知词移除 + "了"净化）
- `analyze_style.py`（419 行）：12 项量化文风指标（句长分布、对话比、
  成语密度、形容词副词密度、身体情绪密度、结构句式检测等）

这是用规则引擎替代 agent 判断力。WVP 的做法是列 5 条反模式让 agent
自己判断，效果等价，维护成本为零。

### 改动

删掉 `anti-ai.yaml.template` 和 `analyze_style.py`，在 review 子技能的
自检清单里加一段手检条目：

```markdown
### AI 味自检（读完一章后逐项过）
- [ ] 「了」字病：每段不超过 2 个"了"
- [ ] 感知词模板：「感到/看到/听到/闻到/想到」——超过 1 处就改
- [ ] 「不是……而是……」句式：全文不超过 1 处
- [ ] 身体部位+情绪模板：「心头一紧」「嘴角上扬」「眼眶一热」
- [ ] 副词密度：每 100 字不超过 3 个「地」
- [ ] 对话占比：正文 ≥ 30%，不低于 20%
```

### 影响范围

- 删除 `scripts/templates/anti-ai.yaml.template`（284 行）
- 删除 `scripts/analyze_style.py`（419 行）
- 修改 `skills/review/` 的自检清单
- 删除 `scripts/check_completeness.py` 中对 analyze_style 的调用（如有）
- 删除 `install.sh` 中对这两个文件的拷贝

---

## 3. Phase 4 合并到 Phase 3

### 现状问题

`skills/prompt/` 是一个独立的子技能，但它的 SKILL.md 描述是"手动调整
提示词（正常流程自动执行）"。一个"自动执行"的阶段不需要独立存在。

### 改动

Phase 3（outline）的最后一步自然产出提示词。在 outline 子技能的工作流
末尾加一段：

```
3.4 自动组装章提示词
    根据 writing-style.yaml 四个字段 + prompt_segment +
    本章章纲，自动写入 prompts/vol-N-ch-M-prompt.md
    视角转换需经作者确认（见上）
```

### 影响范围

- 删除 `skills/prompt/` 子技能和 SKILL.md
- 修改主 SKILL.md 的 Phase 描述（Phase 4 条目改为指向 Phase 3 末尾）
- 修改 install.sh 中的拷贝列表

---

## 4. 安装脚本清理

### 现状问题

install.sh 的 include list 包含即将删除的文件和目录。

### 改动

从 install.sh 的拷贝列表中移除：
- `scripts/templates/anti-ai.yaml.template`
- `scripts/analyze_style.py`
- `skills/prompt/`

---

## 不动部分

| 组件 | 原因 |
|---|---|
| SKILL.md 136 行 | 已经够精简 |
| story.yaml / hooks.yaml | 小说图状结构的必要状态 |
| writing-style.yaml 4 字段 | 等同 WVP 的 theme token，领域必须 |
| 15 项质量检查 | 和 WVP 的 17 条自检都在同一粒度 |
| skills/write/ / archive/ / review/ | 核心工作流，没有过度工程 |
| 6 phase 大框架 | 和 WVP 的 4 phase 复杂度同级 |

---

## 收益估算

| 项 | 已审阅的删除 | 代码删除 |
|---|---|---|
| Genre corpus 继承 | 7 个 variant 文件 | ~200 行 YAML |
| 反 AI 味检测 | anti-ai.yaml.template + analyze_style.py | ~700 行代码 |
| Phase 4 合并 | 删 skills/prompt/ | ~1 个子技能 |
| **总计** | **~700 行 + 1 个子技能** | **Infra 减 ~40%** |

产出质量和用户写作体验不变。改动集中在 agent 看不到的底层架构建模。

---

## 风险

1. **合并 variant 时的字段重复**：人工合并 14 个 variant 到各自基类，
   确保不丢字段。单文件更简单所以更容易校验完整性。
2. **删除 analyze_style.py 后失去量化反馈**：量化指标的缺失由 reviewer
   agent 的 checklist 补偿。agent 的判断力比脚本的 pattern match 更灵活。
3. **Phase 4 合并后视角确认节点可能被跳过**：在 SKILL.md 的 Phase 3
   描述中显式保留"视角转换需经作者确认"的约束。
