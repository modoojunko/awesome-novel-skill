# hooks.yaml - 伏笔/钩子追踪
# 基于 InkOS Hook Lifecycle + webnovel-writer Reading Power Taxonomy
# 追踪跨章节伏笔的全生命周期：pending → mentioned → resolved → abandoned

hooks:
  # 每个钩子有完整生命周期状态
  # id: 唯一标识
  # description: 钩子内容描述（一句话）
  # introduced_in: 引入章节（vol-ch 格式）
  # status: pending | mentioned | resolved | abandoned
  # payoff_timing: immediate（1-3章内）| near_term（5-10章内）| mid_arc（本卷内）| slow_burn（跨卷）| endgame（终局）
  # priority: 1（核心主线）| 2（重要支线）| 3（可选伏笔）
  # hook_type: mystery（悬念）| threat（威胁）| promise（承诺）| clue（线索）| relationship（关系伏笔）| power（能力伏笔）| emotion（情绪钩-愤怒/心疼/共情驱动）| choice（选择钩-两难抉择驱动）| desire（渴望钩-期待兑现驱动）
  # hook_strength: strong（卷末/关键转折）| medium（普通章）| weak（过渡章）
  # hook_position: chapter_end（章末驱动点下一章）| in_chapter（章内保持沉浸）| both
  # last_mentioned_chapter: 最近一次被提及的章节
  # resolution_chapter: 收束的章节（resolved/abandoned 时填写）
  # notes: 额外备注
  - id: ""
    description: ""
    introduced_in: "1-1"
    status: "pending"
    payoff_timing: "near_term"
    priority: 1
    hook_type: "mystery"
    hook_strength: "medium"      # strong | medium | weak
    hook_position: "chapter_end" # chapter_end | in_chapter | both
    seed_text: ""           # 钩子种下时的原文片段（1-3句），用于兑现时锚定读者记忆
    seed_location: ""       # 种下的具体位置（vol-ch 格式）
    last_mentioned_chapter: ""
    resolution_chapter: ""
    notes: ""

# 钩子类型说明（扩展自 webnovel-writer Reading Power Taxonomy）
hook_type_guide:
  mystery:     "悬念钩：信息缺口/未解之谜 → 读者想知道答案"
  threat:      "危机钩：敌人出现/危险逼近 → 读者担心角色安全"
  promise:     "承诺钩：明确预告未来事件 → 读者期待兑现"
  clue:        "线索钩：碎片信息/暗示 → 读者想拼出全貌"
  relationship: "关系钩：角色关系张力/变化 → 读者想看关系走向"
  power:       "能力钩：能力突破/新技能预告 → 读者期待变强"
  emotion:     "情绪钩：触发愤怒/心疼/共情/不公 → 读者想替主角出头或看到正义"
  choice:      "选择钩：两难抉择/高风险决策 → 读者想知道角色怎么选"
  desire:      "渴望钩：奖励/突破/复仇/真相在即 → 读者想看到愿望实现的过程"

# 钩子强度说明
hook_strength_guide:
  strong:  "卷末/关键转折/大冲突前——读者必须立刻知道后续"
  medium:  "普通剧情章——读者想知道，但可以等到下一章"
  weak:    "过渡章/铺垫章——维持阅读惯性即可"

# 钩子健康检查规则（借鉴 InkOS Auditor 的 hook health analysis）
hook_health_rules:
  # 同类型钩子在不同 payoff 区间的合理分布
  payoff_distribution:
    immediate_max: 3     # immediate 区间最多同时存在 3 个未收束钩子
    near_term_max: 5     # near_term 区间最多 5 个
    mid_arc_max: 8       # mid_arc 区间最多 8 个
    slow_burn_max: 5     # slow_burn 区间最多 5 个

  # 钩子陈旧度检测：超过 N 章未被提及的钩子标记为 stale
  stale_threshold:
    high_priority: 5     # 高优先级钩子超过 5 章未提及 → 警告
    normal_priority: 3   # 普通钩子超过 3 章未提及 → 警告

  # 不允许的钩子状态
  no_burst_settlement: true   # 不允许同一章内集中收束 3 个以上钩子
  no_orphan_hooks: true       # 不允许 abandoned 钩子关联到活跃角色/主线

  # 钩子强度分布检查
  strength_distribution:
    max_consecutive_weak: 3    # 连续 weak 钩子不超过 3 章
    require_strong_every: 5    # 每 5 章至少一个 strong 钩子（通常在卷末或关键转折）

# 钩子操作语义（借鉴 InkOS 的 upsert/mention/resolve/defer）
hook_operations:
  upsert: "新增或更新钩子（同一钩子跨章演进时更新描述和 last_mentioned）。新钩子必须在归档时从正文提取 1-3 句原文填入 seed_text"
  mention: "本章提及已有钩子，更新 last_mentioned_chapter"
  resolve: "钩子在当前章收束，填入 resolution_chapter。兑现时必须引用 seed_text 中的原文画面，使兑现段落与种下时的画面形成呼应"
  defer: "钩子收束推迟（需说明理由和新的 payoff 预期）"
  abandon: "废弃钩子（仅当主线方向改变时，需注明原因）"
  extract_seed: "归档时从正文中提取新埋钩子的原文片段（1-3句），填入该钩子的 seed_text 字段"
