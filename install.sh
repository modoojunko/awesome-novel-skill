#!/bin/bash
# Novel Agent Skill 安装脚本

set -e

usage() {
    echo "用法: $0 <平台>"
    echo "平台: claude-code, hermes"
    echo "示例: $0 hermes"
    exit 1
}

if [ $# -lt 1 ]; then
    usage
fi

PLATFORM="$1"

case "$PLATFORM" in
    claude-code)
        DEST_DIR="$HOME/.claude/skills/novel-agent"
        ;;
    hermes)
        DEST_DIR="$HOME/.hermes/skills/novel-agent"
        ;;
    *)
        echo "不支持的平台: $PLATFORM"
        usage
        ;;
esac

echo "安装到: $DEST_DIR"

mkdir -p "$DEST_DIR"
cp SKILL.md "$DEST_DIR/"
cp -r scripts "$DEST_DIR/"

echo "安装完成!"
