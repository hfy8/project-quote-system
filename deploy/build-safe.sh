#!/bin/bash
# build.sh 包装器: 自动清理 CRLF 行尾后执行真正的脚本
# 用法: bash build-safe.sh <版本号> <操作>
# 环境变量: SKIP_LOGIN=1 跳过 Harbor 登录
SELF="$(readlink -f "$0")"
REAL="${SELF%-safe.sh}.sh"

if [ ! -f "$REAL" ]; then
    echo "[ERROR] 找不到 $REAL"
    exit 1
fi

if grep -q $"\r" "$REAL"; then
    echo "[WARN] $REAL 有 CRLF 行尾, 自动清理..."
    cp "$REAL" "${REAL}.bak.$(date +%s)"
    sed -i 's/\r$//' "$REAL"
fi

exec bash "$REAL" "$@"
