#!/bin/bash
# 测试 check_completeness.py — 验证四种场景的输出
#
# 用法: bash scripts/tests/run_tests.sh
# 依赖: example/暗流 项目存在

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CHECK_SCRIPT="$SCRIPT_DIR/../check_completeness.py"
FIXTURES="$SCRIPT_DIR/fixtures"
EXAMPLE="$SCRIPT_DIR/../../example/暗流"
PASS=0
FAIL=0

assert_output() {
    local label="$1"
    local expected="$2"
    local output="$3"

    if echo "$output" | grep -q "$expected"; then
        echo -e "  ${GREEN}PASS${NC} $label"
        PASS=$((PASS + 1))
    else
        echo -e "  ${RED}FAIL${NC} $label"
        echo "    expected to find: $expected"
        echo "    actual output:"
        echo "$output" | sed 's/^/      /'
        FAIL=$((FAIL + 1))
    fi
}

# ── 测试 1: 完整项目 ──────────────────────────────
echo "1. 完整项目 (example/暗流)"
output=$(python3 "$CHECK_SCRIPT" "$EXAMPLE" 2>&1) || true
assert_output "可以进入 Phase 4" "可以进入 Phase 4" "$output"
assert_output "角色文件存在" "个角色文件" "$output"
assert_output "钩子条目存在" "至少一个有效钩子条目" "$output"

# ── 测试 2: 缺失文件 ──────────────────────────────
echo "2. 缺失文件 (hooks.yaml 不存在)"
output=$(python3 "$CHECK_SCRIPT" "$FIXTURES/missing-file" 2>&1) || true
assert_output "报告文件不存在" "文件不存在" "$output"

# ── 测试 3: 无角色文件 ──────────────────────────────
echo "3. 无角色文件 (character-setting 目录为空)"
output=$(python3 "$CHECK_SCRIPT" "$FIXTURES/no-characters" 2>&1) || true
assert_output "报告无角色文件" "无角色文件" "$output"

# ── 测试 4: 非存在目录 ──────────────────────────────
echo "4. 不存在的项目目录"
output=$(python3 "$CHECK_SCRIPT" "/tmp/nonexistent-novel-project-12345" 2>&1) || true
assert_output "报告目录不存在" "项目目录不存在" "$output"

# ── 结果 ──────────────────────────────────────────
echo ""
TOTAL=$((PASS + FAIL))
echo "结果: $PASS/$TOTAL 通过, $FAIL 失败"
if [ "$FAIL" -gt 0 ]; then
    exit 1
fi
