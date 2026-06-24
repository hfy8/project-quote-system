# Docker 部署文档 (v17 FastAPI)

## 部署模式

本项目支持**两种**部署模式：

| 模式 | 脚本 | 适用场景 |
|---|---|---|
| **单机 (Docker compose)** | `docker-deploy.sh` | 本地开发、单机测试 |
| **生产 (Swarm + Harbor)** | `build.sh` | 正式上线, 多节点集群 |

下面分别介绍。

## 目录结构

```
deploy/
├── .env.example          # 环境变量模板（复制为 .env）
├── Dockerfile.backend    # 后端镜像（Python 3.12 + uvicorn :5001）
├── Dockerfile.frontend   # 前端镜像（node构建 + nginx :80）
├── docker-compose.yml    # 单机版编排（db + redis + backend + frontend）
├── docker-deploy.sh      # 单机一键部署脚本
├── build.sh              # Harbor 上传 + Swarm 部署脚本 (生产用)
├── entrypoint.sh         # 后端容器入口（uvicorn 多worker启动）
├── nginx.conf            # 反向代理配置（/api/ → backend:5001）
├── db-init/              # PostgreSQL 初始化 SQL（建 vector 扩展）
│   └── 01-extensions.sql
└── DEPLOY.md             # 本文档
```

## 前提条件

| 条件 | 说明 |
|---|---|
| **Docker** | 已安装（推荐 Docker Desktop + WSL2 集成）|
| **Docker Compose** | V2（`docker compose` 命令）|
| **网络** | 容器能访问 MiniMax/DeepSeek API |

## 服务清单

docker-compose 启动 4 个容器：

| 服务 | 镜像 | 端口 | 作用 |
|---|---|---|---|
| **db** | `pgvector/pgvector:pg16` | 5432 (可选暴露) | PostgreSQL + pgvector |
| **redis** | `redis:7-alpine` | 6379 (内网) | 缓存 (取代本地内存 LRU) |
| **backend** | `python:3.12-slim` 自建 | 5001 (内网) | FastAPI + uvicorn |
| **frontend** | `node:20-alpine` 两阶段 + nginx | 80 (暴露) | Vue3 + 反向代理 |

**Redis 缓存**：
- 自动启用（无需密码，内网通信）
- 后端优先用 Redis；不可用时自动降级到内存 LRU
- 健康检查: `redis-cli ping`

**调试技巧**：
- 想从宿主机连 Redis：`docker compose exec redis redis-cli`
- 想从宿主机连 DB：`docker compose exec db psql -U postgres`

## 快速部署

```bash
# 1. 进入项目根目录
cd /home/rs8568/project-quote-system

# 2. 复制环境变量模板并编辑
cp deploy/.env.example deploy/.env
nano deploy/.env   # 填入真实密码/密钥

# 3. 一键构建+启动
./deploy/docker-deploy.sh up

# 4. 看日志
./deploy/docker-deploy.sh logs
```

## 访问

| 服务 | 地址 |
|---|---|
| 前端页面 | `http://localhost:80`（或 `FRONTEND_PORT`）|
| 后端 API | `http://localhost:5001/api/ai/health` |
| 容器内部 | `backend:5001`（frontend → backend 代理） |

## 常用操作

```bash
# 停止
./deploy/docker-deploy.sh down

# 重建（改代码后）
./deploy/docker-deploy.sh rebuild

# 状态
./deploy/docker-deploy.sh status

# 进入后端容器
./deploy/docker-deploy.sh shell-backend

# 整理（删除所有容器+卷+镜像，数据会丢！）
./deploy/docker-deploy.sh clean
```

## 环境变量

| 变量 | 说明 | 示例 |
|---|---|---|
| `POSTGRES_HOST` | 数据库主机 | `10.60.100.3` |
| `POSTGRES_PORT` | 数据库端口 | `5432` |
| `POSTGRES_DB` | 数据库名 | `quotation_db` |
| `POSTGRES_USER` | 数据库用户 | `postgres` |
| `POSTGRES_PASSWORD` | 数据库密码 | `***` |
| `MINIMAX_API_KEY` | MiniMax API 密钥 | `sk-xxx` |
| `MINIMAX_BASE_URL` | MiniMax API 地址 | `https://api.minimax.chat/v1` |
| `MINIMAX_MODEL` | MiniMax 模型名 | `MiniMax-Text-01` |
| `DEEPSEEK_API_KEY` | DeepSeek 密钥（fallback） | `sk-xxx` |
| `DEEPSEEK_BASE_URL` | DeepSeek API 地址 | `https://api.deepseek.com` |
| `DEEPSEEK_MODEL` | DeepSeek 模型名 | `deepseek-chat` |
| `JWT_SECRET_KEY` | JWT 签名密钥 | 32+字符随机 |
| `SECRET_KEY` | 应用密钥 | 32+字符随机 |
| `UVICORN_WORKERS` | uvicorn worker 数量 | `2` |
| `FRONTEND_PORT` | 前端暴露端口 | `8080` |

## 架构

```
请求 (端口80)
    │
    ▼
┌─── frontend (nginx 容器) ────┐
│  /                  → 静态资源  │
│  /api/...           → proxy    │
└─────────┬───────────────┘
          │ (容器内: backend:5001)
          ▼
┌─── backend (uvicorn 容器) ───┐
│  FastAPI + 41 个 AI 工具     │
│  ┌────────────┐ ┌──────────┐ │
│  │ cache 层   │─│ Redis    │ │
│  │ (LRU 兜底)  │ │ 容器内    │ │
│  └────────────┘ └──────────┘ │
│  logs/ → app.log            │
│  启动时:  init_db.py 创表   │
└─────────┬───────────────┘
          │ (容器内: db:5432)
          ▼
┌─── db (pgvector/pgvector) ───┐
│  PostgreSQL 16 + vector 扩展 │
│  自动:  CREATE EXTENSION     │
│  启动时:  建表 + 基础数据    │
│  持久化:  db_data volume      │
└─────────────────────────────┘
```

## 启动顺序

`docker compose up` 按 `depends_on` 顺序自动:

1. **db** - PostgreSQL 启动 → 执行 `db-init/*.sql` (装 vector 扩展) → healthy
2. **redis** - Redis 启动 → `PING` healthy
3. **backend** - 等待 db+redis healthy → 跑 `init_db.py` (建表+基础数据) → 启动 uvicorn
4. **frontend** - 等待 backend healthy → 启动 nginx

## 首次部署后

admin 用户自动创建，**默认密码 `admin123`**，登录后请立即修改。

数据库是空的，需要 seed 测试数据：

```bash
# 进入 backend 容器
docker compose exec backend bash

# 运行 seed 脚本
python3 scripts/seed_quotations.py
```

## 已有数据的部署

如果 DB 已有数据，不想再 init：

```bash
# .env 文件里
SKIP_DB_INIT=true
```

## 注意事项

1. **日志持久化**：日志目录映射为卷 `backend_logs`，容器重启不丢失
2. **中文字体**：已包含 `fonts/simhei.ttf`，PDF 导出正常
3. **流式 API**：nginx `proxy_buffering off` + 600s 超时，确保 AI SSE 正常工作
4. **健康检查**：后端 `HEALTHCHECK` 依赖 curl，满足后 frontend 才会启动
5. **第一次访问**：需先手动 seed 数据（`python3 scripts/seed_quotations.py`）

---

# 生产部署：Swarm + Harbor

## 流程图

```
开发机 (WSL)
  │
  ├── docker login Harbor
  ├── docker build backend  → 10.60.100.2/rstech_saas/backend:v1.0.0
  ├── docker build frontend → 10.60.100.2/rstech_saas/frontend:v1.0.0
  ├── docker push × 2
  │
  └── ssh 10.60.100.1 (Swarm manager)
       ├── docker login Harbor
       ├── docker stack deploy quote-system
       └── (Swarm 自动从 Harbor pull + 调度到 worker 节点)
```

## 配置 (build.sh 头部)

| 项 | 值 |
|---|---|
| **Harbor** | `10.60.100.2:443` (user: `RS8568`) |
| **镜像命名** | `rstech_saas/backend:vX.Y.Z` / `rstech_saas/frontend:vX.Y.Z` |
| **Swarm Manager** | `10.60.100.1` (user: `rs`) |
| **部署目录** | `/opt/docker-swarm/rstech_saas` |

## 快速部署

```bash
# 完整流程: 登录 Harbor → 构建 → 推送 → 部署 Swarm
./deploy/build.sh v1.0.0 deploy

# 分步:
./deploy/build.sh v1.0.0 build    # 仅构建+推送 (不部署)
./deploy/build.sh v1.0.0 deploy   # 完整流程
./deploy/build.sh v1.0.0 status   # 查看 Swarm service
./deploy/build.sh v1.0.0 rollback # 回滚到上一版本
./deploy/build.sh v1.0.0 clean    # 清理 24h 旧镜像
```

## 部署到 Swarm 后手动步骤

build.sh 会自动生成 `docker-compose.yml` 和 `.env` 模板到 `/opt/docker-swarm/rstech_saas/`，但有几项需要手动确认：

```bash
# SSH 到 manager
ssh rs@10.60.100.1

cd /opt/docker-swarm/rstech_saas

# 1) 复制 db-init (建 vector 扩展)
cp -r /path/to/project-quote-system/deploy/db-init/* db-init/

# 2) 编辑 .env 填入真实密钥
nano .env
#   POSTGRES_PASSWORD=<真实密码>
#   MINIMAX_API_KEY=<真实>
#   DEEPSEEK_API_KEY=<真实>
#   JWT_SECRET_KEY=<随机 32+ 字符>
#   SECRET_KEY=<随机 32+ 字符>
#   DATABASE_URL=postgresql://postgres:mysecretpassword@db:5432/quotation_db
#                  (或外部 PG: postgresql://postgres:mysecretpassword@10.60.100.3:5432/quotation_db)

# 3) 重新部署 (让 .env 生效)
docker stack deploy -c docker-compose.yml quote-system --with-registry-auth
```

## .env base64 编码说明

`build.sh` 自动生成的 `.env` 是用 **base64 编码** 的真值（避免 git/工具中 redaction 误吃敏感行）：

- ✅ `mysecretpassword` 保真
- ✅ `sk-cp-...` (MiniMax 125 字符 key) 保真
- ✅ `sk-cb9f5...` (DeepSeek 35 字符 key) 保真
- ✅ `hermes-debug-2024` (DEBUG_TOKEN) 保真

如果需要修改密钥，编辑 `backend_fastapi/.env` 本地真值，**重新跑 `bash deploy/build.sh vX.Y.Z deploy`** 会自动重新生成 base64 编码的远程 .env。

## Swarm Service 状态

```bash
# 列出所有 service
docker stack services quote-system

# 列出所有 task (容器)
docker stack ps quote-system

# 看某个 service 日志
docker service logs quote-system_backend

# 看某个 task 日志
docker service logs <task-id>
```

## 架构 (Swarm 部署)

```
┌─────── 10.60.100.2 (Harbor) ───────┐
│  rstech_saas/backend:v1.0.0        │
│  rstech_saas/frontend:v1.0.0       │
└────────────────┬───────────────────┘
                 │ pull
                 ▼
┌─────── Swarm Manager (10.60.100.1) ──────┐
│  Stack: quote-system                      │
│  ├─ db      (pgvector/pgvector:pg16)      │
│  ├─ redis   (redis:7-alpine)              │
│  ├─ backend × 2 (FastAPI + uvicorn)       │
│  └─ frontend × 2 (nginx + Vue)            │
│      端口 80 暴露                          │
└──────┬────────────────────┬───────────────┘
       │                    │
   Worker 1            Worker 2
   (任务调度)           (任务调度)
```

## 注意事项 (Swarm)

1. **db 节点约束**：Swarm overlay 网络对 db 有要求, db/redis 限制在 manager 节点 (`node.role == manager`) — 修改 compose 让 db 也能放到 worker
2. **`--with-registry-auth`**：让 manager 能用本地凭据从 Harbor pull
3. **首次部署**：会触发 init_db.py 自动建表, 第二次会跳过 (用 `pg_isready` healthcheck 等)
4. **回滚**：`docker service rollback quote-system_backend` — 用 Swarm 自带 rollback
5. **重新部署**：`./deploy/build.sh v1.0.1 deploy` 会触发 rolling update (parallelism=1 delay=10s)
