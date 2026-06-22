# Docker 部署文档 (v17 FastAPI)

## 目录结构

```
deploy/
├── .env.example          # 环境变量模板（复制为 .env）
├── Dockerfile.backend    # 后端镜像（Python 3.12 + uvicorn :5001）
├── Dockerfile.frontend   # 前端镜像（node构建 + nginx :80）
├── docker-compose.yml    # 单机编排（不含DB容器）
├── docker-deploy.sh      # 一键部署脚本
├── entrypoint.sh         # 后端容器入口（uvicorn 多worker启动）
├── nginx.conf            # 反向代理配置（/api/ → backend:5001）
└── build.sh              # 旧版（Harbor ← 已废弃，参考用）
```

## 前提条件

| 条件 | 说明 |
|---|---|
| **Docker** | 已安装（推荐 Docker Desktop + WSL2 集成）|
| **Docker Compose** | V2（`docker compose` 命令）|
| **远程 PostgreSQL** | `10.60.100.3:5432/quotation_db`（已有数据）|
| **网络** | 容器能访问 MiniMax/DeepSeek API |

> ⚠️ 本项目**不使用容器内的 PostgreSQL**（复用 10.60.100.3），
> docker-compose.yml 中**不包含 db 服务**。

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
┌─────── frontend (nginx) ───────┐
│  /                  → 静态资源  │
│  /api/...           → proxy    │
└─────────┬──────────────────────┘
           │ (容器内: backend:5001)
           ▼
┌─────── backend (uvicorn) ──────┐
│  FastAPI + 39个 AI 工具        │
│  logs/ → app.log               │
└─────────┬──────────────────────┘
           │ (远程: 10.60.100.3:5432)
           ▼
┌─────── PostgreSQL ─────────────┐
│  quotation_db  (36个报价单)    │
└────────────────────────────────┘
```

## 注意事项

1. **日志持久化**：日志目录映射为卷 `backend_logs`，容器重启不丢失
2. **中文字体**：已包含 `fonts/simhei.ttf`，PDF 导出正常
3. **流式 API**：nginx `proxy_buffering off` + 600s 超时，确保 AI SSE 正常工作
4. **健康检查**：后端 `HEALTHCHECK` 依赖 curl，满足后 frontend 才会启动
5. **第一次访问**：需先手动 seed 数据（`python3 scripts/seed_quotations.py`）
