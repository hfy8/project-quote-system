#!/bin/bash
cd ~/build_ctx/frontend
echo "=== 构建前端镜像 ==="
echo "Fuqiang123##" | sudo -S docker build -t 10.60.100.2/rstech_saas/frontend:v1.3.39 -f Dockerfile.swarm . 2>&1
