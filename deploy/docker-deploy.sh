#!/bin/bash
# ===========================================
# Project Quote System - 一键 Docker 部署
# 用法:
#   ./deploy/docker-deploy.sh up       # 构建+启动
#   ./deploy/docker-deploy.sh down     # 停止
#   ./deploy/docker-deploy.sh logs     # 看日志
#   ./deploy/docker-deploy.sh rebuild  # 重新构建
#   ./deploy/docker-deploy.sh status   # 查看状态
# ===========================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "${SCRIPT_DIR}")"
cd "${PROJECT_DIR}/deploy"

# 颜色
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
log_info()  { echo -e "${GREEN}[INFO]${NC}  $1"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC}  $1"; }
log_err()   { echo -e "${RED}[ERROR]${NC} $1"; }

# 检查 .env
if [ ! -f .env ]; then
    log_warn ".env 不存在，从 .env.example 复制"
    cp .env.example .env
    log_warn "请编辑 .env 填入真实密码/密钥后重跑"
    exit 1
fi

# 加载环境变量
set -a
source .env
set +a

ACTION=${1:-up}

case "${ACTION}" in
    up)
        log_info "1/3 构建镜像..."
        docker compose build
        
        log_info "2/3 启动服务..."
        docker compose up -d
        
        log_info "3/3 等待健康检查..."
        sleep 10
        docker compose ps
        echo ""
        log_info "✅ 部署完成！"
        echo "   前端:  http://localhost:${FRONTEND_PORT:-80}"
        echo "   后端:  http://localhost:5001/api/ai/health"
        ;;
    down)
        log_info "停止服务..."
        docker compose down
        ;;
    logs)
        docker compose logs -f
        ;;
    rebuild)
        log_info "重新构建..."
        docker compose down
        docker compose build --no-cache
        docker compose up -d
        ;;
    status)
        docker compose ps
        echo "---"
        docker compose logs --tail=20
        ;;
    shell-backend)
        docker compose exec backend /bin/bash
        ;;
    shell-frontend)
        docker compose exec frontend /bin/sh
        ;;
    shell-redis)
        docker compose exec redis redis-cli
        ;;
    shell-db)
        docker compose exec db psql -U ${POSTGRES_USER:-postgres} -d ${POSTGRES_DB:-quotation_db}
        ;;
    cache-stats)
        # 调用后端 debug 端点看 cache 命中率
        TOKEN=${DEBUG_TOKEN:-hermes-debug-2024}
        docker compose exec backend curl -s -H "X-Debug-Token: $TOKEN" http://localhost:5001/api/_debug/cache-stats | python3 -m json.tool
        ;;
    clean)
        log_warn "将删除容器+卷+镜像（数据会丢）"
        read -p "确认? (y/N) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            docker compose down -v --rmi all
            log_info "清理完成"
        fi
        ;;
    *)
        echo "用法: $0 {up|down|logs|rebuild|status|shell-backend|shell-frontend|shell-redis|shell-db|cache-stats|clean}"
        exit 1
        ;;
esac
