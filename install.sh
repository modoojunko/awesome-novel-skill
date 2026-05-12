#!/bin/bash
# Novel Agent Skill 安装脚本
#
# awesome-novel-skill - AI-assisted novel writing workflow system
# Copyright (C) 2026  modoojunko
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

set -e

usage() {
    echo "用法: $0 <平台>"
    echo "平台: claude-code, hermes, openclaw, deepseek-tui"
    exit 1
}

if [ $# -lt 1 ]; then
    usage
fi

PLATFORM="$1"

case "$PLATFORM" in
    claude-code)
        SKILLS_DIR="$HOME/.claude/skills"
        ;;
    hermes)
        SKILLS_DIR="$HOME/.hermes/skills"
        ;;
    openclaw)
        SKILLS_DIR="$HOME/.openclaw/skills"
        ;;
    deepseek-tui)
        SKILLS_DIR="$HOME/.deepseek/skills"
        ;;
    *)
        echo "不支持的平台: $PLATFORM"
        usage
        ;;
esac

DEST="$SKILLS_DIR/awesome-novel"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "安装到: $DEST"
export NOVEL_SKILL_HOME="$DEST"

# 将 NOVEL_SKILL_HOME 写入 profile 文件，确保所有 shell 类型可用
for profile_file in "$HOME/.profile" "$HOME/.bashrc"; do
    if ! grep -q "export NOVEL_SKILL_HOME" "$profile_file" 2>/dev/null; then
        echo "export NOVEL_SKILL_HOME=\"$DEST\"" >> "$profile_file"
        echo "已添加 NOVEL_SKILL_HOME=$DEST 到 $profile_file"
    fi
done

# 安全检查：DEST 不能为空、不能是根目录、路径中必须包含 awesome-novel
if [[ -z "$DEST" || "$DEST" == "/" || "$DEST" != *awesome-novel* ]]; then
    echo "错误：安装目标路径异常 ($DEST)，中止。"
    exit 1
fi

# 创建技能目录，已存在则清空
rm -rf "$DEST"
mkdir -p "$DEST"

# 只复制运行时需要的文件（include list，避免泄露仓库元数据）
cp "$SCRIPT_DIR/SKILL.md" "$DEST/"
cp -r "$SCRIPT_DIR/scripts" "$DEST/"
cp -r "$SCRIPT_DIR/skills" "$DEST/"
cp -r "$SCRIPT_DIR/agents" "$DEST/"
cp -r "$SCRIPT_DIR/references" "$DEST/"

echo "安装完成!"
