#!/bin/bash
# 启动后端，日志重定向到 logs/app.log（同时保留 stdout）
# 用法: ./start.sh
set -e
cd "$(dirname "$0")"
mkdir -p logs
LOG_FILE="logs/app.log"
echo "🚀 启动后端 (port 5001) — 日志输出: $LOG_FILE + stdout"
python3 -m uvicorn main:fastapi_app --host=0.0.0.0 --port 5001 2>&1 | tee -a "$LOG_FILE"
