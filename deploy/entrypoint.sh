#!/bin/bash
set -e

echo "等待数据库就绪..."
sleep 5

echo "初始化数据库..."
cd /app
python init_db.py

echo "启动 Flask..."
exec flask run --host 0.0.0.0
