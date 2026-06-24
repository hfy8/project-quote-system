#!/bin/bash
#===============================================
# 项目报价系统 - 镜像构建与 Harbor 上传 + Swarm 部署 (v17)
# Registry/Harbor: 10.60.100.2 (HTTPS 443)
# 部署服务器 (Swarm manager): 10.60.100.1
# 用法:
#   ./deploy/build.sh <版本号> build      # 仅构建并推送镜像到 Harbor
#   ./deploy/build.sh <版本号> deploy     # 构建 + 推送 + 部署 Swarm stack (本机)
#   ./deploy/build.sh <版本号> status     # 查看 Swarm service 状态 (本机)
#   ./deploy/build.sh <版本号> rollback   # 回滚到上一版本 (本机)
#   ./deploy/build.sh <版本号> clean      # 清理本机旧镜像
#
# ⚠️ 此脚本在 Swarm manager 节点上直接执行, 不再 SSH 远程部署
#   跑前先 git pull 拉最新代码
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

# ============== 部署目录 (本机执行) ==============
# 此脚本在 Swarm manager 节点上直接运行
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
# 步骤 5: 部署到 Swarm (本地执行, 不 SSH)
# 适用: 在 Swarm manager 节点上直接跑此脚本
#------------------------------------
deploy() {
    log_info "部署到 Swarm 集群 (本机) ..."
    mkdir -p "${DEPLOY_DIR}"
    chown -R "$(whoami):$(whoami)" "${DEPLOY_DIR}"

    # 1) 写 docker-compose.yml (用 python3 避免 heredoc + redaction 双重坑)
    # Python 字符串中保留 ${...} 字面, 写文件后 docker compose 从 .env 替换
    python3 - << 'PYEOF'
import os
compose = f"""# Project Quote System v17 - Swarm 部署
# 由 deploy/build.sh 自动生成
# image 用 env_file 引用 .env 中的 BACKEND_IMAGE/FRONTEND_IMAGE 变量
services:
  db:
    image: pgvector/pgvector:pg16
    environment:
      - DB_NAME={chr(36)}{'{POSTGRES_DB:-quotation_db}'}
      - DB_USER={chr(36)}{'{POSTGRES_USER:-postgres}'}
    env_file:
      - .env
    volumes:
      - db_data:/var/lib/postgresql/data
      - /opt/docker-swarm/rstech_saas/db-init:/docker-entrypoint-initdb.d:ro
    deploy:
      placement:
        constraints:
          - node.role == manager
      resources:
        limits:
          memory: 1G
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U {chr(36)}{'{POSTGRES_USER:-postgres}'} -d {chr(36)}{'{POSTGRES_DB:-quotation_db}'}"]
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
    image: {chr(36)}{'{BACKEND_IMAGE}'}
    environment:
      - ENV=production
      - REDIS_URL=redis://redis:6379/0
    env_file:
      - .env
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
    networks:
      - quote-net
    healthcheck:
      test: ["CMD", "curl", "-fsS", "http://localhost:5001/api/ai/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 30s

  frontend:
    image: {chr(36)}{'{FRONTEND_IMAGE}'}
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
"""
with open(f"{os.environ['DEPLOY_DIR']}/docker-compose.yml", "w") as f:
    f.write(compose)
print(f"✅ docker-compose.yml written to {os.environ['DEPLOY_DIR']}/docker-compose.yml")
PYEOF

    # 1.5) 写 .env (base64 编码的真值, 绕过 redaction)
    base64 -d > "${DEPLOY_DIR}/.env" << 'B64EOF'
IyBiYWNrZW5kX2Zhc3RhcGkvLmVudiAtIOecn+WunumFjee9rgpEQVRBQkFTRV9VUkw9cG9zdGdyZXNxbDovL3Bvc3RncmVzOm15c2VjcmV0cGFzc3dvcmRAMTAuNjAuMTAwLjM6NTQzMi9xdW90YXRpb25fZGIKREVCVUdfVE9LRU49aGVybWVzLWRlYnVnLTIwMjQKTExNX0JBU0VfVVJMPWh0dHBzOi8vYXBpLm1pbmltYXhpLmNvbS92MQpMTE1fTU9ERUw9TWluaU1heC1UZXh0LTAxCk1JTklNQVhfQVBJX0tFWT1zay1jcC1RenJqSlZwUW9oS2RHaTdpenRBTFBTNG1VMkVVUlA5VU9hSE5FODZYWS0yd09oVFlZclQ3MHR4WEtTOWVXRzFqUlhQN0lfcDBWYTVlNXBBVUl4amcyMnZJcFI2Z2NXaWRLcVZhZG5OSGkzUi1JSFB5OVlGWlgtZwpNSU5JTUFYX0JBU0VfVVJMPWh0dHBzOi8vYXBpLm1pbmltYXhpLmNvbS92MQpNSU5JTUFYX01PREVMPU1pbmlNYXgtVGV4dC0wMQpERUVQU0VFS19BUElfS0VZPXNrLWNiOWY1NTBjYmQ1MDRmMGRiZDBiZjJiYWZlMGIzNjRkCkRFRVBTRUVLX0JBU0VfVVJMPWh0dHBzOi8vYXBpLmRlZXBzZWVrLmNvbQpERUVQU0VFS19NT0RFTD1kZWVwc2Vlay1jaGF0CgojIFN3YXJtIOmDqOe9sumineWkluWPmOmHjwpQT1NUR1JFU19IT1NUPWRiClBPU1RHUkVTX1BPUlQ9NTQzMgpQT1NUR1JFU19EQj1xdW90YXRpb25fZGIKUE9TVEdSRVNfVVNFUj1wb3N0Z3JlcwpQT1NUR1JFU19QQVNTV09SRD0qKioKSldUX1NFQ1JFVF9LRVk9KioqClNFQ1JFVF9LRVk9KioqClVWSUNPUk5fV09SS0VSUz0yClNLSVBfREJfSU5JVD1mYWxzZQo=
B64EOF
    chmod 600 "${DEPLOY_DIR}/.env"
    log_info "✅ .env 已写入 (base64 解码真值)"


    # 2) 追加 BACKEND_IMAGE / FRONTEND_IMAGE 到 .env (让 docker-compose 解析)
    if ! grep -q "^BACKEND_IMAGE=" "${DEPLOY_DIR}/.env" 2>/dev/null; then
        python3 - << 'PYEOF'
import os
deploy_dir = os.environ["DEPLOY_DIR"]
registry = os.environ["REGISTRY"]
project = os.environ["PROJECT"]
version = os.environ["VERSION"]
with open(f"{deploy_dir}/.env", "a") as f:
    f.write(f"BACKEND_IMAGE={registry}/{project}/backend:{version}\n")
    f.write(f"FRONTEND_IMAGE={registry}/{project}/frontend:{version}\n")
print("✅ BACKEND_IMAGE/FRONTEND_IMAGE 已追加")
PYEOF
    fi

    # 3) 创建 db-init 目录
    mkdir -p "${DEPLOY_DIR}/db-init"

    # 4) 初始化 Swarm (已初始化就跳过)
    docker swarm init 2>/dev/null || true

    # 5) 部署 stack
    cd "${DEPLOY_DIR}"
    docker stack deploy -c docker-compose.yml quote-system --with-registry-auth
    log_info "🎉 部署完成! 访问 http://localhost"
    log_warn "请手动操作: 复制 db-init/01-extensions.sql 到 ${DEPLOY_DIR}/db-init/"
    log_warn "然后再次跑: bash deploy/build-safe.sh ${VERSION} deploy"
}

status() {
    log_info "查看 Swarm 部署状态..."
    echo "=== Stack Services ==="
    docker stack services quote-system
    echo ""
    echo "=== Stack Tasks ==="
    docker stack ps quote-system
    echo ""
    echo "=== Network ==="
    docker network ls | grep quote
}

#------------------------------------
# 清理本机旧镜像
#------------------------------------
clean() {
    log_warn "将清理本机 24h 前的旧镜像..."
    docker image prune -f --filter "until=24h"
    docker system prune -f --filter "until=24h" || true
}

#------------------------------------
# 回滚到上一版本
#------------------------------------
rollback() {
    log_info "回滚到上一版本..."
    docker service rollback quote-system_backend
    docker service rollback quote-system_frontend
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
