"""FastAPI 应用入口 - v4（最终版）

策略：
- 启动时立即 create Flask app（让所有 SQLAlchemy model 注册）
- 把 Flask app 绑到 FastAPI 启动时的依赖
- FastAPI 路由里所有 DB 操作通过 Depends(get_db) 走 flask_app.app_context()
- 老 Flask 路由用 WSGIMiddleware 挂载在 /legacy/*
- 不再做 sys.modules 注入（避免双重 import）
"""
import os
import sys
import logging

# 关键：backend/ 在 sys.path，让 backend.app.create_app() 内部的 'app.xxx' 引用能找到
BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))
sys.path.insert(0, BACKEND_DIR)

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from contextlib import asynccontextmanager
from typing import Optional
from datetime import datetime, timedelta

logger = logging.getLogger("fastapi-app")
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(name)s: %(message)s')


# ============== 加载 Flask 后端（启动时） ==============
import importlib.util

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
BACKEND_DIR = os.path.join(PROJECT_ROOT, 'backend')

# backend/ 不是 package，把 backend 加到 sys.path
sys.path.insert(0, BACKEND_DIR)

# 现在可以直接 `from app.xxx` 加载
import app as app_module  # = backend.app.__init__
import app.config as config_module

Config = config_module.Config
create_flask_app = app_module.create_app

# 先创建 Flask app（这一步注册所有 SQLAlchemy models 到 metadata）
_flask_app = create_flask_app()
logger.info(f"✅ Flask app created: {Config.SQLALCHEMY_DATABASE_URI[:50]}...")


# ============== DB Session 依赖 ==============
# Flask-SQLAlchemy 的 session 绑定到 app context。
# 整个进程共用一个 app context（FastAPI 通常是 async 但 DB 操作是 sync 跑在 thread pool）
_app_ctx = _flask_app.app_context()
_app_ctx.push()  # 进程级，常驻


def get_db():
    """FastAPI 依赖：app context 已在启动时 push，直接返回 session"""
    from app import db
    yield db.session


# ============== JWT（FastAPI 自己的鉴权） ==============
from jose import jwt, JWTError
# 关键：用 Config.JWT_SECRET_KEY（不是 SECRET_KEY），与 Flask-JWT-Extended 一致
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
    yield
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


# ============== 全局异常处理：Flask 兼容格式 ==============
# 把 FastAPI 默认的 {"detail": "..."} 转成 Flask 的 {"error": "..."}
# 这样前端 axios 拦截器无需区分 FastAPI/Flask

from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError

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
def health():
    return {
        "status": "ok",
        "version": "2.1.0-fastapi",
        "auth_implemented": "fastapi",
        "legacy_count": 131,
    }


# ============== 注册 FastAPI 原生 auth 路由 ==============
from api_app.api.auth import router as auth_router
from api_app.api.materials import router as materials_router
from api_app.api.modules import router as modules_router
from api_app.api.quotations import router as quotations_router
fastapi_app.include_router(auth_router, prefix="/api/auth", tags=["认证"])
fastapi_app.include_router(materials_router, prefix="/api/materials", tags=["物料库"])
# module_bp 注册到 /api 蓝本（Flask 同 prefix）
fastapi_app.include_router(modules_router, prefix="/api", tags=["模块"])
# quotation_bp 注册到 /api 蓝本（Flask 同 prefix）
fastapi_app.include_router(quotations_router, prefix="/api", tags=["报价单"])


# ============== 挂载 Flask 老路由到 /legacy ==============
from a2wsgi import WSGIMiddleware
fastapi_app.mount("/legacy", WSGIMiddleware(_flask_app))
logger.info("✅ Flask legacy app mounted at /legacy (131 endpoints)")


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
    uvicorn.run("api_app.main:fastapi_app", host="0.0.0.0", port=5001, reload=False, log_level="info")