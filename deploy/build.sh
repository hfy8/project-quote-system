#!/bin/bash
#===============================================
# 项目报价系统 - 镜像构建与 Harbor 上传 + Swarm 部署 (v17)
# Registry/Harbor: 10.60.100.2 (HTTPS 443)
# 部署服务器 (Swarm manager): 10.60.100.1
# 用法:
#   ./deploy/build.sh <版本号> build      # 仅构建并推送镜像到 Harbor
#   ./deploy/build.sh <版本号> deploy     # 构建 + 推送 + 部署 Swarm stack
#   ./deploy/build.sh <版本号> status     # 查看 Swarm service 状态
#   ./deploy/build.sh <版本号> rollback   # 回滚到上一版本
#   ./deploy/build.sh <版本号> clean      # 清理服务器旧镜像
#
# ⚠️ 必须用 bash 跑 (脚本用 bash 特性):
#   bash ./deploy/build.sh v1.0.0 deploy
#   或 chmod +x 后 ./build.sh v1.0.0 deploy
#===============================================

# 强制使用 bash (防止 sh/dash 调用)
if [ -z "$BASH_VERSION" ]; then
    echo "[ERROR] 必须用 bash 跑此脚本, 不要再用 sh"
    echo "        用法: bash $0 $@"
    exit 1
fi

set -e

# ============== 配置 ==============
REGISTRY="10.60.100.2"
# 注意: REGISTRY_PORT 仅用于 docker login 时的 URL, 不放在镜像 tag 中
REGISTRY_PORT="443"
REGISTRY_URL="${REGISTRY}:${REGISTRY_PORT}"
PROJECT="rstech_saas"
VERSION=${1:-"v1.0.0"}
# 镜像 tag 用纯 hostname (不带 :443)
BACKEND_IMAGE="${REGISTRY}/${PROJECT}/backend:${VERSION}"
FRONTEND_IMAGE="${REGISTRY}/${PROJECT}/frontend:${VERSION}"

HARBOR_USER="RS8568"
HARBOR_PASS="Bj6546321."

# TLS 跳过 (Harbor 自签名证书)
# 方案: 用 insecure-registry (在 /etc/docker/daemon.json 配)
#       或 用环境变量 DOCKER_CONTENT_TRUST=0 + DOCKER_TLS_VERIFY=0
SKIP_TLS_VERIFY=${SKIP_TLS_VERIFY:-0}

# 部署服务器 (Swarm manager)
SSH_HOST="10.60.100.1"
SSH_USER="rs"
SSH_PASS="Fuqiang123##"
DEPLOY_DIR="/opt/docker-swarm/${PROJECT}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "${SCRIPT_DIR}")"
BUILD_CONTEXT="${PROJECT_ROOT}"

# 颜色
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
log_info()  { echo -e "${GREEN}[INFO]${NC}  $1"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC}  $1"; }
log_err()   { echo -e "${RED}[ERROR]${NC} $1"; }

#------------------------------------
# 步骤 1: 登录 Harbor (本地)
# 失败时回退到 insecure-registry 重试
#------------------------------------
login_harbor() {
    log_info "登录 Harbor ${REGISTRY_URL}..."
    if echo "${HARBOR_PASS}" | docker login "${REGISTRY_URL}" -u "${HARBOR_USER}" --password-stdin 2>/dev/null; then
        return 0
    fi
    # 失败: 配 insecure-registry (Harbor 自签名证书)
    log_warn "TLS 证书校验失败, 切换为 insecure-registry 模式..."
    DOCKER_DAEMON_JSON="/etc/docker/daemon.json"
    if [ -f "${DOCKER_DAEMON_JSON}" ]; then
        cp "${DOCKER_DAEMON_JSON}" "${DOCKER_DAEMON_JSON}.bak.$(date +%s)"
    fi
    # 用 python 写 json (避免 bash 解析)
    if command -v python3 >/dev/null 2>&1; then
        python3 << PYEOF
import json, os
p = "/etc/docker/daemon.json"
try:
    with open(p) as f:
        cfg = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    cfg = {}
cfg.setdefault("insecure-registries", [])
url = "${REGISTRY}"
if url not in cfg["insecure-registries"]:
    cfg["insecure-registries"].append(url)
with open(p, "w") as f:
    json.dump(cfg, f, indent=2)
print(f"已写入 {p}: insecure-registries={cfg['insecure-registries']}")
PYEOF
        if [ $? -ne 0 ]; then
            log_err "写入 daemon.json 失败, 请手动配置 insecure-registry: ${REGISTRY}"
            return 1
        fi
    else
        log_err "需要 python3 来配置 daemon.json, 请手动加 insecure-registry: ${REGISTRY}"
        return 1
    fi
    # 重启 docker
    log_warn "重启 docker..."
    systemctl restart docker || service docker restart || true
    sleep 3
    # 重试 login
    echo "${HARBOR_PASS}" | docker login "${REGISTRY_URL}" -u "${HARBOR_USER}" --password-stdin
}

#------------------------------------
# 步骤 2: 构建后端镜像
#------------------------------------
build_backend() {
    log_info "构建后端镜像: ${BACKEND_IMAGE}"
    docker build -t "${BACKEND_IMAGE}" \
        -f "${PROJECT_ROOT}/deploy/Dockerfile.backend" \
        "${PROJECT_ROOT}"
    log_info "✅ 后端镜像构建完成"
}

#------------------------------------
# 步骤 3: 构建前端镜像
#------------------------------------
build_frontend() {
    log_info "构建前端镜像: ${FRONTEND_IMAGE}"
    docker build -t "${FRONTEND_IMAGE}" \
        -f "${PROJECT_ROOT}/deploy/Dockerfile.frontend" \
        "${PROJECT_ROOT}"
    log_info "✅ 前端镜像构建完成"
}

#------------------------------------
# 步骤 4: 推送镜像到 Harbor
#------------------------------------
push_images() {
    log_info "推送后端镜像 ${BACKEND_IMAGE} ..."
    docker push "${BACKEND_IMAGE}"
    log_info "✅ 后端镜像已上传 Harbor"

    log_info "推送前端镜像 ${FRONTEND_IMAGE} ..."
    docker push "${FRONTEND_IMAGE}"
    log_info "✅ 前端镜像已上传 Harbor"
}

#------------------------------------
# 步骤 5: 部署到 Swarm
#------------------------------------
deploy() {
    log_info "部署到 Swarm 集群 ${SSH_HOST} ..."

    sshpass -p "${SSH_PASS}" ssh -o StrictHostKeyChecking=no "${SSH_USER}@${SSH_HOST}" "
        set -e
        echo '${HARBOR_PASS}' | docker login ${REGISTRY_URL} -u '${HARBOR_USER}' --password-stdin

        sudo mkdir -p ${DEPLOY_DIR}
        sudo chown -R ${SSH_USER}:${SSH_USER} ${DEPLOY_DIR}

        cat > ${DEPLOY_DIR}/docker-compose.yml << 'COMPOSE_EOF'
# Project Quote System v17 - Swarm 部署
# 由 deploy/build.sh 自动生成
services:
  db:
    image: pgvector/pgvector:pg16
    environment:
      - POSTGRES_DB=\${POSTGRES_DB:-quotation_db}
      - POSTGRES_USER=\${POSTGRES_USER:-postgres}
      - POSTGRES_PASSWORD=\${POSTGRES_PASSWORD:-CHANGEME}
    volumes:
      - db_data:/var/lib/postgresql/data
      - \${DEPLOY_DIR}/db-init:/docker-entrypoint-initdb.d:ro
    deploy:
      placement:
        constraints:
          - node.role == manager
      resources:
        limits:
          memory: 1G
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U \${POSTGRES_USER:-postgres} -d \${POSTGRES_DB:-quotation_db}"]
      interval: 10s
      timeout: 5s
      retries: 10
      start_period: 20s
    networks:
      - quote-net

  redis:
    image: redis:7-alpine
    command: ["redis-server", "--save", "60", "1", "--loglevel", "warning"]
    volumes:
      - redis_data:/data
    deploy:
      placement:
        constraints:
          - node.role == manager
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5
    networks:
      - quote-net

  backend:
    image: \${BACKEND_IMAGE}
    environment:
      - ENV=production
      - DATABASE_URL=\${DATABASE_URL}
      - REDIS_URL=redis://redis:6379/0
      - LLM_BASE_URL=\${MINIMAX_BASE_URL}
      - LLM_MODEL=\${MINIMAX_MODEL}
      - MINIMAX_API_KEY=\${MINIMAX_API_KEY}
      - DEEPSEEK_API_KEY=\${DEEPSEEK_API_KEY}
      - JWT_SECRET_KEY=\${JWT_SECRET_KEY}
      - SECRET_KEY=\${SECRET_KEY}
      - UVICORN_WORKERS=\${UVICORN_WORKERS:-2}
    volumes:
      - backend_logs:/app/logs
    deploy:
      replicas: 2
      update_config:
        parallelism: 1
        delay: 10s
      restart_policy:
        condition: on-failure
        max_attempts: 3
      resources:
        limits:
          memory: 1G
    # 注意: Swarm 不支持 depends_on (用 healthcheck + 重试来确保依赖)
    networks:
      - quote-net
    healthcheck:
      test: ["CMD", "curl", "-fsS", "http://localhost:5001/api/ai/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 30s

  frontend:
    image: \${FRONTEND_IMAGE}
    deploy:
      replicas: 2
      update_config:
        parallelism: 1
        delay: 10s
      restart_policy:
        condition: on-failure
        max_attempts: 3
      resources:
        limits:
          memory: 256M
    ports:
      - target: 80
        published: 80
        protocol: tcp
        mode: host
    # 注意: Swarm 不支持 depends_on
    networks:
      - quote-net
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://localhost/healthz"]
      interval: 30s
      timeout: 5s
      retries: 3

volumes:
  db_data:
  redis_data:
  backend_logs:

networks:
  quote-net:
    driver: overlay
COMPOSE_EOF

        cat > \${DEPLOY_DIR}/.env << 'ENVEOF'
# Project Quote System v17 - Swarm .env
POSTGRES_DB=quotation_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=CHANGEME_password
DATABASE_URL=postgresql://postgres:POSTGRES_PASSWORD@db:5432/quotation_db
MINIMAX_API_KEY=CHANGEME_minimax_key
DEEPSEEK_API_KEY=CHANGEME_deepseek_key
JWT_SECRET_KEY=CHANGEME_jwt_secret
SECRET_KEY=CHANGEME_app_secret
MINIMAX_BASE_URL=https://api.minimaxi.com/v1
MINIMAX_MODEL=MiniMax-Text-01
SKIP_DB_INIT=false
UVICORN_WORKERS=2
ENVEOF

        mkdir -p \${DEPLOY_DIR}/db-init

        docker swarm init 2>/dev/null || true
        cd \${DEPLOY_DIR}
        docker stack deploy -c docker-compose.yml quote-system --with-registry-auth
        echo '=== 部署完成 ==='
    "

    log_info "🎉 部署完成! 访问 http://\${SSH_HOST}"
    log_warn "请确保 10.60.100.1:\${DEPLOY_DIR}/db-init/ 已复制 db-init/01-extensions.sql"
    log_warn "请确保 10.60.100.1:\${DEPLOY_DIR}/.env 已填入真实密钥"
}

#------------------------------------
# 部署状态
#------------------------------------
status() {
    log_info "查看 Swarm 部署状态..."
    sshpass -p "${SSH_PASS}" ssh -o StrictHostKeyChecking=no "${SSH_USER}@${SSH_HOST}" "
        echo '=== Stack Services ==='
        docker stack services quote-system
        echo ''
        echo '=== Stack Tasks ==='
        docker stack ps quote-system
        echo ''
        echo '=== Network ==='
        docker network ls | grep quote
    "
}

#------------------------------------
# 清理服务器旧镜像
#------------------------------------
clean() {
    log_warn "将清理服务器 24h 前的旧镜像..."
    sshpass -p "${SSH_PASS}" ssh -o StrictHostKeyChecking=no "${SSH_USER}@${SSH_HOST}" "
        docker image prune -f --filter 'until=24h'
        docker system prune -f --filter 'until=24h' || true
    "
}

#------------------------------------
# 回滚到上一版本
#------------------------------------
rollback() {
    log_info "回滚到上一版本..."
    sshpass -p "${SSH_PASS}" ssh -o StrictHostKeyChecking=no "${SSH_USER}@${SSH_HOST}" "
        docker service rollback quote-system_backend
        docker service rollback quote-system_frontend
    "
}

#==========================================
# 主流程
#==========================================
ACTION=${2:-"deploy"}
SKIP_LOGIN=${SKIP_LOGIN:-0}

case "${ACTION}" in
    build)
        if [ "${SKIP_LOGIN}" != "1" ]; then login_harbor; else log_info "跳过 Harbor 登录 (SKIP_LOGIN=1)"; fi
        build_backend
        build_frontend
        push_images
        log_info "🎉 镜像构建并上传 Harbor 完成"
        ;;
    deploy)
        if [ "${SKIP_LOGIN}" != "1" ]; then login_harbor; else log_info "跳过 Harbor 登录 (SKIP_LOGIN=1)"; fi
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
        echo "流程:"
        echo "  1) build   = 登录 Harbor → 构建 backend/frontend 镜像 → 推送到 Harbor"
        echo "  2) deploy  = build + SSH 到 Swarm manager → 部署 stack"
        echo "  3) status  = 查看 Swarm service 状态"
        echo "  4) clean   = 清理服务器 24h 前的旧镜像"
        echo "  5) rollback= 回滚 backend/frontend 到上一版本"
        echo ""
        echo "示例:"
        echo "  $0 v1.0.0 build    # 仅构建并推送镜像到 Harbor"
        echo "  $0 v1.0.0 deploy   # 构建 + 推送 + 部署"
        echo "  $0 v1.0.0 status   # 查看 Swarm 状态"
        echo "  $0 v1.0.0 rollback # 回滚到上一版本"
        exit 1
        ;;
esac
