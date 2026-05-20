#!/bin/bash
#===============================================
# 项目报价系统 - 镜像构建与部署脚本
# Registry/Harbor: 10.60.100.2 (HTTPS 443)
# 部署服务器: 10.60.100.1
#===============================================

set -e

# 配置
REGISTRY="10.60.100.2"
PROJECT="project-quote"
VERSION=${1:-"v1.0.0"}
BACKEND_IMAGE="${REGISTRY}/${PROJECT}/backend:${VERSION}"
FRONTEND_IMAGE="${REGISTRY}/${PROJECT}/frontend:${VERSION}"
SSH_HOST="10.60.100.1"
SSH_USER="root"
SSH_PASS="Fuqiang123##"
DEPLOY_DIR="/opt/docker-swarm/${PROJECT}"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_err() { echo -e "${RED}[ERROR]${NC} $1"; }

#------------------------------------------
# 步骤1: 登录 Harbor
#------------------------------------------
login_harbor() {
    log_info "登录 Harbor..."
    echo "Bj6546321" | docker login ${REGISTRY} -u "RS8568" --password-stdin
}

#------------------------------------------
# 步骤2: 构建后端镜像
#------------------------------------------
build_backend() {
    log_info "构建后端镜像: ${BACKEND_IMAGE}"
    docker build -t ${BACKEND_IMAGE} \
        -f deploy/Dockerfile.backend \
        ./backend
    log_info "后端镜像构建完成"
}

#------------------------------------------
# 步骤3: 构建前端镜像
#------------------------------------------
build_frontend() {
    log_info "构建前端镜像: ${FRONTEND_IMAGE}"
    docker build -t ${FRONTEND_IMAGE} \
        -f deploy/Dockerfile.frontend \
        .
    log_info "前端镜像构建完成"
}

#------------------------------------------
# 步骤4: 推送镜像到 Harbor
#------------------------------------------
push_images() {
    log_info "推送镜像到 Harbor..."
    docker push ${BACKEND_IMAGE}
    docker push ${FRONTEND_IMAGE}
    log_info "镜像推送完成"
}

#------------------------------------------
# 步骤5: 部署到服务器
#------------------------------------------
deploy() {
    log_info "部署到服务器 ${SSH_HOST}..."

    sshpass -p "${SSH_PASS}" ssh -o StrictHostKeyChecking=no ${SSH_USER}@${SSH_HOST} "
        # 登录 Harbor
        echo 'Bj6546321' | docker login ${REGISTRY} -u 'RS8568' --password-stdin

        # 创建部署目录
        mkdir -p ${DEPLOY_DIR}

        # 复制 docker-compose.yml 和配置文件
        cat > ${DEPLOY_DIR}/docker-compose.yml << 'EOF'
version: '3.8'
services:
  backend:
    image: ${REGISTRY}/${PROJECT}/backend:${VERSION}
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=postgresql://postgres:Quote2024@db:5432/quotation_db
      - JWT_SECRET_KEY=${JWT_SECRET:-quote-jwt-secret-2024}
      - SECRET_KEY=${SECRET_KEY:-quote-secret-2024}
    deploy:
      replicas: 2
      update_config:
        parallelism: 1
        delay: 10s
      restart_policy:
        condition: on-failure
        max_attempts: 3
    depends_on:
      db:
        condition: service_healthy
    networks:
      - quote-net
    healthcheck:
      test: [\"CMD\", \"curl\", \"-f\", \"http://localhost:5000/api/quotations\"]
      interval: 30s
      timeout: 10s
      retries: 3

  frontend:
    image: ${REGISTRY}/${PROJECT}/frontend:${VERSION}
    deploy:
      replicas: 2
      restart_policy:
        condition: on-failure
    networks:
      - quote-net

  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_DB=quotation_db
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=Quote2024
    volumes:
      - pgdata:/var/lib/postgresql/data
    deploy:
      resources:
        limits:
          memory: 512M
    healthcheck:
      test: [\"CMD-SHELL\", \"pg_isready -U postgres\"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - quote-net

volumes:
  pgdata:

networks:
  quote-net:
    driver: overlay
EOF

        # 初始化 swarm（如果需要）
        docker swarm init 2>/dev/null || true

        # 部署 stack
        cd ${DEPLOY_DIR}
        docker stack deploy -c docker-compose.yml quote-system --with-registry-auth

        log_info '部署完成!'
    "

    log_info "部署完成！访问 http://${SSH_HOST}"
}

#------------------------------------------
# 步骤6: 查看部署状态
#------------------------------------------
status() {
    log_info "查看部署状态..."
    sshpass -p "${SSH_PASS}" ssh -o StrictHostKeyChecking=no ${SSH_USER}@${SSH_HOST} "
        docker stack ps quote-system
        echo '---'
        docker service ls
    "
}

#------------------------------------------
# 清理旧镜像
#------------------------------------------
clean() {
    log_info "清理服务器上的旧镜像..."
    sshpass -p "${SSH_PASS}" ssh -o StrictHostKeyChecking=no ${SSH_USER}@${SSH_HOST} "
        docker system prune -f --filter 'until=24h' || true
    "
}

#------------------------------------------
# 回滚到上一版本
#------------------------------------------
rollback() {
    log_info "回滚到上一版本..."
    sshpass -p "${SSH_PASS}" ssh -o StrictHostKeyChecking=no ${SSH_USER}@${SSH_HOST} "
        docker service rollback quote-system/backend
        docker service rollback quote-system/frontend
    "
}

#==========================================
# 主流程
#==========================================
ACTION=${2:-"deploy"}

case ${ACTION} in
    build)
        login_harbor
        build_backend
        build_frontend
        push_images
        ;;
    deploy)
        login_harbor
        build_backend
        build_frontend
        push_images
        deploy
        ;;
    status)
        status
        ;;
    clean)
        clean
        ;;
    rollback)
        rollback
        ;;
    *)
        echo "用法: $0 <版本号> <操作>"
        echo ""
        echo "  版本号: 如 v1.0.0, latest (默认: v1.0.0)"
        echo "  操作:   build | deploy | status | clean | rollback"
        echo ""
        echo "示例:"
        echo "  $0 v1.0.0 build    # 仅构建并推送镜像"
        echo "  $0 v1.0.0 deploy   # 构建、推送并部署"
        echo "  $0 v1.0.0 status   # 查看部署状态"
        echo "  $0 v1.0.0 rollback # 回滚服务"
        exit 1
        ;;
esac
