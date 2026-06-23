# Docker 部署文档 (v17 FastAPI)

## 目录结构

```
deploy/
├── .env.example          # 环境变量模板（复制为 .env）
├── Dockerfile.backend    # 后端镜像（Python 3.12 + uvicorn :5001）
├── Dockerfile.frontend   # 前端镜像（node构建 + nginx :80）
├── docker-compose.yml    # 单机编排（db + redis + backend + frontend）
├── docker-deploy.sh      # 一键部署脚本
├── entrypoint.sh         # 后端容器入口（uvicorn 多worker启动）
├── nginx.conf            # 反向代理配置（/api/ → backend:5001）
├── db-init/              # PostgreSQL 初始化 SQL（建 vector 扩展）
│   └── 01-extensions.sql
└── build.sh              # 旧版（Harbor ← 已废弃，参考用）
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
