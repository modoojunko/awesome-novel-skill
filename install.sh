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
    echo "平台: claude-code, hermes, openclaw"
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
    *)
        echo "不支持的平台: $PLATFORM"
        usage
        ;;
esac

DEST="$SKILLS_DIR/awesome-novel"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "安装到: $DEST"

# 全量覆盖
rm -rf "$DEST"
cp -r "$SCRIPT_DIR" "$DEST"

# 清理不需要的文件
rm -rf "$DEST/.git" "$DEST/.claude" "$DEST/docs" "$DEST/example"

echo "安装完成!"
