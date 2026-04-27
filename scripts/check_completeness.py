#!/usr/bin/env python3
# awesome-novel-skill - AI-assisted novel writing workflow system
# Copyright (C) 2026  modoojunko
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
"""
导入完整性检查 —— 扫描项目 YAML 文件，标记空字段和缺失文件。

用法:
    python check_completeness.py [项目路径]
"""

import sys
from pathlib import Path

# 尝试导入 yaml，失败则用 json
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False
    import json


def load_yaml(path: Path) -> dict | None:
    """加载 YAML 文件，返回 dict 或 None"""
    if not path.exists():
        return None
    if HAS_YAML:
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
    else:
        # JSON 模式下，返回基本结构供检查
        return {"_raw": path.read_text(encoding='utf-8')}


EXPECTED = {
    "world-setting.yaml": {
        "path": "settings/world-setting.yaml",
        "fields": ["geography", "politics", "culture", "history", "rules", "physics", "biology", "sociology"],
    },
    "writing-style.yaml": {
        "path": "settings/writing-style.yaml",
        "fields": ["role", "core_principles", "possible_mistakes", "depiction_techniques"],
    },
    "hooks.yaml": {
        "path": "settings/hooks.yaml",
        "check": lambda d: len(d.get("hooks", [])) > 0 and d["hooks"][0].get("id") not in (None, ""),
        "label": "至少一个有效钩子条目",
    },
    "character-setting": {
        "path": "settings/character-setting/",
        "check": lambda d: sum(1 for f in Path(str(d["_path"]) if isinstance(d.get("_path"), str) else (
            Path(sys.argv[1]) / "settings/character-setting" if len(sys.argv) > 1 else Path(".")
        )).glob("*.yaml") if f.is_file() if f.is_file()),
        "label": "至少一个角色文件",
        "is_dir": True,
    },
}


def check_empty_fields(data: dict, fields: list[str], parent: str = "details") -> list[dict]:
    """检查嵌套字段中的空值"""
    results = []
    source = data.get(parent, data)
    if not isinstance(source, dict):
        source = data
    for field in fields:
        if field in source:
            val = source[field]
            empty = val is None or (isinstance(val, str) and val.strip() == "") or (isinstance(val, list) and len(val) == 0)
        else:
            empty = True
        results.append({
            "field": f"{parent}.{field}" if parent else field,
            "empty": empty,
        })
    return results


def main():
    if len(sys.argv) < 2:
        print("用法: python check_completeness.py [项目路径]")
        sys.exit(1)

    project = Path(sys.argv[1])
    if not project.exists():
        print(f"错误：项目目录不存在: {sys.argv[1]}")
        sys.exit(1)

    total_ok = 0
    total_warn = 0
    total_miss = 0

    for name, spec in EXPECTED.items():
        filepath = project / spec["path"]
        print(f"## {spec['path']}")

        if spec.get("is_dir"):
            char_dir = project / spec["path"]
            yaml_files = list(char_dir.glob("*.yaml")) if char_dir.exists() else []
            if yaml_files:
                print(f"  ✅ {len(yaml_files)} 个角色文件: {', '.join(f.name for f in yaml_files)}")
                total_ok += 1
            else:
                print(f"  ❌ 无角色文件——Phase 4 写作时角色行为无约束")
                total_miss += 1
            continue

        if not filepath.exists():
            print(f"  ❌ 文件不存在")
            total_miss += 1
            continue

        data = load_yaml(filepath)
        if data is None:
            print(f"  ❌ 文件无法解析")
            total_miss += 1
            continue

        if "check" in spec:
            ok = spec["check"](data)
            if ok:
                print(f"  ✅ {spec['label']}")
                total_ok += 1
            else:
                print(f"  ❌ {spec['label']}")
                total_miss += 1
            continue

        for r in check_empty_fields(data, spec["fields"]):
            if r["empty"]:
                print(f"  ❌ {r['field']}: 空")
                total_miss += 1
            else:
                total_ok += 1
                # Don't print every OK field to keep output concise

    print(f"\n---")
    print(f"✅ {total_ok} 项就绪  ⚠️ 0 项待确认  ❌ {total_miss} 项缺失")

    if total_miss > 0:
        print(f"\n建议：先补关键项再进入 Phase 4，缺失字段会导致 subagent 写作时自行猜测。")
    else:
        print("可以进入 Phase 4。")


if __name__ == "__main__":
    main()
