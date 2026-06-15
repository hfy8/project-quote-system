"""FastAPI 通用依赖：DB session + JWT 鉴权

独立模块 - 避免 main.py 与 api/*.py 之间的循环导入

使用：
    from core.auth import get_db, get_current_user_id, create_access_token
"""
from typing import Optional
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

from db import db_session_factory
from core.config import Config


# ============== DB Session ==============
def get_db():
    """FastAPI 依赖：返回当前线程的 SQLAlchemy session"""
    session = db_session_factory()
    try:
        yield session
    except Exception:
        session.rollback()
        raise


# ============== JWT（FastAPI 自己的鉴权） ==============
JWT_SECRET = Config.JWT_SECRET_KEY
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24


def create_access_token(identity: str) -> str:
    """生成 JWT access token"""
    expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    payload = {"sub": str(identity), "exp": expire, "iat": datetime.utcnow()}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_access_token(token: str) -> Optional[str]:
    """解码 JWT token，返回 user_id (str) 或 None"""
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM]).get("sub")
    except JWTError:
        return None


# ============== FastAPI 依赖：获取当前用户 ID ==============
bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user_id(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
) -> str:
    """从 Authorization Header 解出 user_id"""
    if not credentials or not credentials.credentials:
        raise HTTPException(status_code=401, detail="缺少认证信息")
    user_id = decode_access_token(credentials.credentials)
    if not user_id:
        raise HTTPException(status_code=401, detail="Token 无效或已过期")
    return user_id
