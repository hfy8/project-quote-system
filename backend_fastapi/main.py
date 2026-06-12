"""FastAPI 应用入口 - v17（无 Flask + 整理后结构）

策略：
- 启动时导入 core.models 注册所有 SQLAlchemy models 到 metadata
- 用 db 模块提供的纯 SQLAlchemy 2.x 引擎 + session
- FastAPI 路由里所有 DB 操作通过 Depends(get_db) 走 session
- 不再创建 Flask app，/legacy 挂载已移除
"""
import os
import sys
import logging

# 关键：backend_fastapi/ 在 sys.path，让 core/db/utils 引用能找到
# uvicorn 启动时 cwd 通常是项目根（不是 backend_fastapi/），所以这里手动插入
BACKEND_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, BACKEND_DIR)

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from contextlib import asynccontextmanager
from typing import Optional
from datetime import datetime, timedelta
from decimal import Decimal
import json

logger = logging.getLogger("fastapi-app")
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(name)s: %(message)s')


# ============== 加载后端（启动时） ==============
# 这一步会触发 core 包导入所有 models（注册到 ModuleBase.metadata）
from db import db, engine
from core.config import Config
import core  # 触发 core/__init__.py 导入所有 models

logger.info(f"✅ DB engine created: {Config.SQLALCHEMY_DATABASE_URI[:50]}...")


# ============== DB Session 依赖 ==============
from db import db_session_factory


def get_db():
    """FastAPI 依赖：返回当前线程的 SQLAlchemy session"""
    session = db_session_factory()
    try:
        yield session
    except Exception:
        session.rollback()
        raise


# ============== JWT（FastAPI 自己的鉴权） ==============
from jose import jwt, JWTError
JWT_SECRET = Config.JWT_SECRET_KEY
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24

def create_access_token(identity: str) -> str:
    expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    payload = {"sub": str(identity), "exp": expire, "iat": datetime.utcnow()}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_access_token(token: str) -> Optional[str]:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM]).get("sub")
    except JWTError:
        return None


bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user_id(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
) -> str:
    if not credentials or not credentials.credentials:
        raise HTTPException(status_code=401, detail="缺少认证信息")
    user_id = decode_access_token(credentials.credentials)
    if not user_id:
        raise HTTPException(status_code=401, detail="Token 无效或已过期")
    return user_id


# ============== App ==============
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 FastAPI 启动")

    # 启动后台定时任务
    import os
    _scheduler = None
    if os.environ.get("FASTAPI_OWNS_SCHEDULER", "1") == "1":
        try:
            from apscheduler.schedulers.background import BackgroundScheduler
            from apscheduler.triggers.cron import CronTrigger
            from core.tasks.sync_task import sync_all, cleanup_expired_messages

            _scheduler = BackgroundScheduler()

            # 每天 22:00 数据同步（SQL Server → PostgreSQL）
            _scheduler.add_job(
                func=sync_all,
                trigger=CronTrigger(hour=22, minute=0),
                id='daily_sync',
                name='每日数据同步',
                replace_existing=True,
            )

            # 每天 03:00 清理过期消息
            _scheduler.add_job(
                func=cleanup_expired_messages,
                trigger=CronTrigger(hour=3, minute=0),
                id='message_cleanup',
                name='清理过期消息',
                replace_existing=True,
            )

            _scheduler.start()
            logger.info("✅ 定时任务已启动：22:00 数据同步 / 03:00 清理过期消息")
        except Exception as e:
            logger.exception(f"⚠️ 定时任务启动失败: {e}")

    yield

    # 关闭时停止 scheduler
    if _scheduler is not None:
        try:
            _scheduler.shutdown(wait=False)
            logger.info("⏹ 定时任务调度器已停止")
        except Exception:
            pass

    logger.info("👋 FastAPI 关闭")


fastapi_app = FastAPI(
    title="项目报价系统 API (FastAPI 版)",
    version="2.1.0-fastapi",
    description="""
# 项目报价系统 - FastAPI 渐进迁移版

## 双栈运行
- **FastAPI**（新）：原生 Python 类型 + 自动文档（/docs）
- **Flask**（老）：通过 WSGIMiddleware 挂载在 `/legacy/*`，行为完全保留

## 迁移进度（当前 1/20 域）
| 域 | 端点数 | 状态 |
|----|--------|------|
| auth | 4 | ✅ FastAPI |
| 其他 19 域 | 127 | ⏳ Flask legacy |

## 鉴权
- 两个栈共用同一 `SECRET_KEY`，JWT 可互用
- Flask 端走原 `@jwt_required`，FastAPI 端走 `Depends(get_current_user_id)`
""",
    lifespan=lifespan,
)

fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 中间件：注入请求 context 到 utils.logger（替代 flask.request 全局）
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class RequestContextMiddleware(BaseHTTPMiddleware):
    """每个请求把 Request 注入到线程本地，供 log_operation 获取 IP/UA"""
    async def dispatch(self, request: Request, call_next):
        from utils.logger import set_request_context
        set_request_context(request)
        try:
            return await call_next(request)
        finally:
            # 清理（防止 thread pool 复用）
            from utils.logger import _local
            if hasattr(_local, "request"):
                delattr(_local, "request")


fastapi_app.add_middleware(RequestContextMiddleware)


# 全局异常处理：Flask 兼容格式
# 把 FastAPI 默认的 {"detail": "..."} 转成 Flask 的 {"error": "..."}
# 这样前端 axios 拦截器无需区分 FastAPI/Flask

from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError

# 自定义 JSON 编码器：处理 Decimal 等类型
class DecimalJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)

# 覆写 FastAPI 的默认 JSONResponse 序列化
# Starlette 用 json.dumps 序列化，我们可以 monkey-patch 让 fastapi.responses.JSONResponse 用自定义 encoder
import fastapi.responses as resp_mod
_orig_dumps = json.dumps
def _patched_dumps(obj, **kwargs):
    kwargs.setdefault('cls', DecimalJSONEncoder)
    return _orig_dumps(obj, **kwargs)
json.dumps = _patched_dumps

async def http_exception_handler(request, exc):
    """HTTPException -> {"error": detail}"""
    detail = exc.detail if isinstance(exc.detail, str) else str(exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": detail},
    )

fastapi_app.add_exception_handler(StarletteHTTPException, http_exception_handler)
fastapi_app.add_exception_handler(HTTPException, http_exception_handler)


@fastapi_app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    """Pydantic 验证错误 -> {"error": ...}"""
    errors = exc.errors()
    msg = errors[0]["msg"] if errors else "参数错误"
    return JSONResponse(
        status_code=422,
        content={"error": f"参数错误: {msg}"},
    )


# ============== Health ==============
@fastapi_app.get("/health", tags=["系统"])
def health():
    return {
        "status": "ok",
        "version": "2.1.0-fastapi",
        "auth_implemented": "fastapi",
        "legacy_count": 131,
    }


# ============== 注册 FastAPI 原生 auth 路由 ==============
from api.auth import router as auth_router
from api.materials import router as materials_router
from api.modules import router as modules_router
from api.quotations import router as quotations_router
from api.fees import router as fees_router
from api.fee_rates import router as fee_rates_router
from api.labor_hours import router as labor_hours_router
from api.travel_entries import router as travel_entries_router
from api.travel_fees import router as travel_fees_router
from api.exchange_rates import router as exchange_rates_router
from api.logs import router as logs_router
from api.module_participants import router as module_participants_router
from api.sync import router as sync_router
from api.messages import router as messages_router
from api.change_requests import router as change_requests_router
from api.roles import router as roles_router
from api.participant_type_permissions import router as participant_type_permissions_router
from api.users import router as users_router
from api.versions import router as versions_router
from api.exports import router as exports_router
fastapi_app.include_router(auth_router, prefix="/api/auth", tags=["认证"])
fastapi_app.include_router(materials_router, prefix="/api/materials", tags=["物料库"])
# module_bp 注册到 /api 蓝本（Flask 同 prefix）
fastapi_app.include_router(modules_router, prefix="/api", tags=["模块"])
# quotation_bp 注册到 /api 蓝本（Flask 同 prefix）
fastapi_app.include_router(quotations_router, prefix="/api", tags=["报价单"])
fastapi_app.include_router(fees_router, prefix="/api", tags=["其他费用"])
fastapi_app.include_router(fee_rates_router, prefix="/api", tags=["费率"])
fastapi_app.include_router(labor_hours_router, prefix="/api", tags=["人力工时"])
fastapi_app.include_router(travel_entries_router, prefix="/api", tags=["差旅条目"])
fastapi_app.include_router(travel_fees_router, prefix="/api", tags=["差旅配置"])
fastapi_app.include_router(exchange_rates_router, tags=["汇率"])
fastapi_app.include_router(logs_router, tags=["操作日志"])
fastapi_app.include_router(module_participants_router, tags=["模块参与者"])
fastapi_app.include_router(sync_router, prefix="/api/sync", tags=["数据同步"])
fastapi_app.include_router(messages_router, tags=["消息"])
fastapi_app.include_router(change_requests_router, prefix="/api/change-requests", tags=["变更申请"])
fastapi_app.include_router(roles_router, tags=["角色管理"])
fastapi_app.include_router(participant_type_permissions_router, tags=["参与者类型权限"])
fastapi_app.include_router(users_router, tags=["用户管理"])
fastapi_app.include_router(versions_router, tags=["版本快照"])
fastapi_app.include_router(exports_router, tags=["导出"])


# ============== Flask legacy 挂载已移除 ==============
# 老 Flask 路由已全部迁移到 FastAPI（v15 完成）
# 不再需要 WSGIMiddleware 或 a2wsgi


@fastapi_app.get("/", tags=["系统"])
def root():
    return {
        "name": "项目报价系统 API",
        "docs": "/docs",
        "health": "/health",
        "fastapi_endpoints": "/api/auth/* (4 个)",
        "legacy_endpoints": "/legacy/api/* (127 个)",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:fastapi_app", host="0.0.0.0", port=5001, reload=False, log_level="info")