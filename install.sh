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

# 将 NOVEL_SKILL_HOME 写入 profile 文件，支持 bash/zsh/fish
# 先清理旧的 NOVEL_SKILL_HOME 行，避免重装产生重复
for profile_file in "$HOME/.profile" "$HOME/.bashrc" "$HOME/.zshrc"; do
    [ -f "$profile_file" ] || continue
    # 用临时文件清理旧行再写新行
    tmpfile=$(mktemp)
    grep -v "export NOVEL_SKILL_HOME" "$profile_file" > "$tmpfile" 2>/dev/null || true
    echo "export NOVEL_SKILL_HOME=\"$DEST\"" >> "$tmpfile"
    mv "$tmpfile" "$profile_file"
    echo "已更新 NOVEL_SKILL_HOME=$DEST 到 $profile_file"
done

# fish shell 支持（如果存在）
if command -v fish &>/dev/null; then
    fish_conf="$HOME/.config/fish/config.fish"
    if [ -f "$fish_conf" ]; then
        tmpfile=$(mktemp)
        grep -v "set -gx NOVEL_SKILL_HOME" "$fish_conf" > "$tmpfile" 2>/dev/null || true
        echo "set -gx NOVEL_SKILL_HOME \"$DEST\"" >> "$tmpfile"
        mv "$tmpfile" "$fish_conf"
        echo "已更新 NOVEL_SKILL_HOME=$DEST 到 $fish_conf"
    fi
fi

# 安全检查：DEST 必须是以 $HOME 开头的 skills/awesome-novel 路径
CANONICAL_DEST="$(cd "$(dirname "$DEST")" 2>/dev/null && pwd)/$(basename "$DEST")"
if [[ -z "$DEST" || "$DEST" == "/" || "$CANONICAL_DEST" != "$HOME/."*"/skills/awesome-novel" ]]; then
    echo "错误：安装目标路径异常 ($DEST)，中止。"
    exit 1
fi

# 创建技能目录，已存在则清空
rm -rf "$DEST"
mkdir -p "$DEST"

# 复制运行时需要的文件（include list，避免泄露仓库元数据）
cp "$SCRIPT_DIR/SKILL.md" "$DEST/"
cp -r "$SCRIPT_DIR/agents" "$DEST/"
cp -r "$SCRIPT_DIR/skills" "$DEST/"
cp -r "$SCRIPT_DIR/knowledge" "$DEST/"
cp -r "$SCRIPT_DIR/templates" "$DEST/"
cp -r "$SCRIPT_DIR/tools" "$DEST/"
# memory/ 含 writer-style 等静态参考素材，不包含 anti-ai（已迁至 knowledge/anti-ai/）
[ -d "$SCRIPT_DIR/memory" ] && cp -r "$SCRIPT_DIR/memory" "$DEST/"

echo "安装完成!"
