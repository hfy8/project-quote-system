#!/bin/bash
# v17 FastAPI entrypoint
set -e

cd /app

# 输出环境信息
echo "=================================================="
echo "  Project Quote System - Backend (FastAPI v17)"
echo "=================================================="
echo "ENV:        ${ENV:-production}"
echo "DATABASE:   ${DATABASE_URL:-not set}"
echo "LLM_BASE:   ${LLM_BASE_URL:-not set}"
echo "LLM_MODEL:  ${LLM_MODEL:-not set}"
echo "=================================================="

# 校验关键环境变量
if [ -z "$DATABASE_URL" ]; then
    echo "❌ DATABASE_URL is required"
    exit 1
fi

# 启动 uvicorn（生产用多 worker）
WORKERS=${UVICORN_WORKERS:-2}
HOST=0.0.0.0
PORT=5001

echo "🚀 启动 uvicorn on ${HOST}:${PORT} (workers=${WORKERS})"
exec uvicorn main:fastapi_app \
    --host ${HOST} \
    --port ${PORT} \
    --workers ${WORKERS} \
    --log-level info \
    --access-log \
    --proxy-headers \
    --forwarded-allow-ips='*'
