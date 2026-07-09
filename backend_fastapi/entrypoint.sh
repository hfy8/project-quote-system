#!/bin/bash
# v17 FastAPI entrypoint (Docker 部署)
# 启动流程:
#   1. 等待 PostgreSQL 就绪
#   2. 跑 init_db.py (建 pgvector 扩展 + 建表 + 基础数据)
#   3. 启动 uvicorn (多 worker)
set -e

cd /app

# ============== 输出环境信息 ==============
echo "=================================================="
echo "  Project Quote System - Backend (FastAPI v17)"
echo "=================================================="
echo "ENV:        ${ENV:-production}"
echo "DATABASE:   ${DATABASE_URL%%@*}@<hidden>"
echo "LLM_MODEL:  ${LLM_MODEL:-MiniMax-Text-01}"
echo "WORKERS:    ${UVICORN_WORKERS:-2}"
echo "=================================================="

# ============== 校验关键环境变量 ==============
if [ -z "$DATABASE_URL" ]; then
    echo "❌ DATABASE_URL is required"
    exit 1
fi

# ============== 1. 等待 PostgreSQL ==============
DB_HOST=$(echo $DATABASE_URL | sed -E 's|.*@([^:]+):.*|\1|')
DB_PORT=$(echo $DATABASE_URL | sed -E 's|.*:([0-9]+)/.*|\1|')

echo "⏳ 等待 PostgreSQL ${DB_HOST}:${DB_PORT}..."
for i in {1..30}; do
    if pg_isready -h "$DB_HOST" -p "$DB_PORT" -U postgres >/dev/null 2>&1; then
        echo "   ✅ PostgreSQL 已就绪"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "❌ PostgreSQL 等待超时 (30s)"
        exit 1
    fi
    sleep 1
done

# ============== 2. 跑 init_db.py ==============
# 只在 SKIP_DB_INIT 不为 true 时执行（已有数据的部署可跳过）
if [ "${SKIP_DB_INIT:-false}" != "true" ]; then
    echo "🔧 初始化数据库（建表 + 基础数据）..."
    python3 scripts/init_db.py || {
        echo "❌ init_db.py 失败"
        exit 1
    }
    echo "   ✅ 数据库初始化完成"
else
    echo "⏭️  跳过 init_db (SKIP_DB_INIT=true)"
fi

# ============== 3. 启动 uvicorn ==============
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
