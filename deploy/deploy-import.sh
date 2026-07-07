#!/bin/bash
set -e
echo "=== 1. 构建 frontend 镜像 ==="
rsync -avz --delete /home/rs8568/project-quote-system/frontend/dist/ rs@10.60.100.2:~/build_ctx/frontend/dist/ 2>&1 | tail -3
sshpass -f /tmp/.swarmpwd ssh -T -o StrictHostKeyChecking=no -o LogLevel=ERROR rs@10.60.100.2 '
  cd ~/build_ctx/frontend
  sudo docker build -t 10.60.100.2/rstech_saas/frontend:v1.3.39 -f Dockerfile.swarm .
  sudo docker push 10.60.100.2/rstech_saas/frontend:v1.3.39
' 2>&1 | tail -5

echo "=== 2. scp 更新的 backend ==="
# 复制到远端 build_ctx
rsync -az --delete /home/rs8568/project-quote-system/backend_fastapi/ rs@10.60.100.2:~/build_ctx/backend_fastapi/ 2>&1 | tail -3

# 构建 backend
sshpass -f /tmp/.swarmpwd ssh -T -o StrictHostKeyChecking=no -o LogLevel=ERROR rs@10.60.100.2 '
  cd ~/build_ctx/backend_fastapi
  sudo docker build -t 10.60.100.2/rstech_saas/backend:v1.4.24 -f Dockerfile.swarm .
  sudo docker push 10.60.100.2/rstech_saas/backend:v1.4.24
' 2>&1 | tail -5

echo "=== 3. scp stack yml 到 swarm01 ==="
scp /home/rs8568/project-quote-system/deploy/docker-compose.swarm.yml rs@10.60.100.1:~/docker-swarm/rstech_saas/docker-compose.swarm.yml 2>&1 | tail -2

echo "=== 4. 更新版本号 ==="
sshpass -f /tmp/.swarmpwd ssh -T -o StrictHostKeyChecking=no -o LogLevel=ERROR rs@10.60.100.1 '
  sed -i "s|backend:v[0-9.]*|backend:v1.4.24|g" ~/docker-swarm/rstech_saas/docker-compose.swarm.yml
  sed -i "s|frontend:v[0-9.]*|frontend:v1.3.39|g" ~/docker-swarm/rstech_saas/docker-compose.swarm.yml
  echo "版本更新后:"
  grep -E "image:" ~/docker-swarm/rstech_saas/docker-compose.swarm.yml
' 2>&1 | tail -5

echo "=== 5. 部署到 swarm ==="
sshpass -f /tmp/.swarmpwd ssh -T -o StrictHostKeyChecking=no -o LogLevel=ERROR rs@10.60.100.1 '
  cd ~/docker-swarm/rstech_saas
  docker stack deploy -c docker-compose.swarm.yml quote-system
  sleep 5
  echo "=== 部署状态 ==="
  docker service ls --filter name=quote-system
' 2>&1 | tail -15

echo "=== 6. 强制滚动更新 backend ==="
sshpass -f /tmp/.swarmpwd ssh -T -o StrictHostKeyChecking=no -o LogLevel=ERROR rs@10.60.100.1 '
  docker service update --force quote-system_backend
  sleep 3
  docker service ps quote-system_backend
' 2>&1 | tail -10