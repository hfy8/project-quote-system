"""
debug 端点
- /cache-stats: 缓存命中率/keys
- /config: 当前生效的环境配置 (脱敏)
"""
import os
from fastapi import APIRouter, HTTPException, Header
from core.services.cache import cache_stats, _memory

router = APIRouter(prefix="/api/_debug", tags=["debug"])
# 优先从环境变量 DEBUG_TOKEN 读
TOKEN = os.environ.get("DEBUG_TOKEN")
if TOKEN is None:
    # 生产环境必须设 DEBUG_TOKEN
    _is_prod = not os.environ.get("FLASK_ENV") or os.environ.get("FLASK_ENV") == "production"
    if _is_prod:
        raise RuntimeError("Fatal: DEBUG_TOKEN not set in production!")
    TOKEN = "hermes-debug-2024"


def _redact(value):
    """敏感字段脱敏 - 把真实密钥打码"""
    if value is None:
        return None
    s = str(value)
    # 敏感字段: 密码/密钥 全部打码
    sensitive = [
        os.environ.get("POSTGRES_PASSWORD", ""),
        os.environ.get("MYSEKRET", ""),
        os.environ.get("MINIMAX_API_KEY", ""),
        os.environ.get("LLM_API_KEY", ""),
        os.environ.get("DEEPSEEK_API_KEY", ""),
        os.environ.get("JWT_SECRET_KEY", ""),
        os.environ.get("SECRET_KEY", ""),
        os.environ.get("DEBUG_TOKEN", ""),
    ]
    # 也尝试从 DATABASE_URL 里提取密码
    db_url = os.environ.get("DATABASE_URL", "")
    if db_url and "@" in db_url:
        # postgresql://user:password@host:port/db
        try:
            userinfo = db_url.split("//", 1)[1].split("@", 1)[0]
            if ":" in userinfo:
                pwd = userinfo.split(":", 1)[1]
                if pwd and len(pwd) >= 4:
                    sensitive.append(pwd)
        except Exception:
            pass
    for sec in sensitive:
        if sec and len(sec) >= 4 and sec in s:
            s = s.replace(sec, "***")
    return s


@router.get("/cache-stats")
def get_cache_stats(x_debug_token: str = Header(None)):
    if x_debug_token != TOKEN:
        raise HTTPException(status_code=403, detail="forbidden")

    stats = cache_stats()
    stats["_memory_keys"] = list(_memory._data.keys())[:20] if hasattr(_memory, "_data") else []
    stats["_memory_size"] = len(_memory._data) if hasattr(_memory, "_data") else 0
    stats["_memory_max"] = getattr(_memory, "_max_size", None)
    return stats


@router.get("/config")
def get_config(x_debug_token: str = Header(None)):
    """返回当前生效的环境配置 (敏感值脱敏)"""
    if x_debug_token != TOKEN:
        raise HTTPException(status_code=403, detail="forbidden")

    def env(k, default=""):
        return os.environ.get(k, default)

    return {
        "DATABASE_URL": _redact(env("DATABASE_URL") or env("SQLALCHEMY_DATABASE_URI")),
        "DB_HOST": env("POSTGRES_HOST", "localhost"),
        "DB_PORT": env("POSTGRES_PORT", "5432"),
        "DB_NAME": env("POSTGRES_DB", "quotation_db"),
        "DB_USER": env("POSTGRES_USER", "postgres"),
        "REDIS_URL": _redact(env("REDIS_URL") or "redis://localhost:6379/0"),
        "REDIS_PORT_HOST": env("REDIS_PORT_HOST", "(内网)"),
        "CACHE_DEFAULT_TTL": env("CACHE_DEFAULT_TTL", "30"),
        "CACHE_DISABLED": env("CACHE_DISABLED", "false"),
        "LLM_BASE_URL": env("LLM_BASE_URL", "https://api.minimax.chat/v1"),
        "LLM_MODEL": env("LLM_MODEL", "MiniMax-Text-01"),
        "LLM_API_KEY": "***" if env("LLM_API_KEY") or env("MINIMAX_API_KEY") else "(未设置)",
        "MINIMAX_BASE_URL": env("MINIMAX_BASE_URL", "https://api.minimax.chat/v1"),
        "MINIMAX_MODEL": env("MINIMAX_MODEL", "MiniMax-Text-01"),
        "MINIMAX_API_KEY": "***" if env("MINIMAX_API_KEY") else "(未设置)",
        "DEEPSEEK_BASE_URL": env("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
        "DEEPSEEK_MODEL": env("DEEPSEEK_MODEL", "deepseek-chat"),
        "DEEPSEEK_API_KEY": "***" if env("DEEPSEEK_API_KEY") else "(未设置)",
        "JWT_SECRET_KEY": "***" if env("JWT_SECRET_KEY") else "(默认值)",
        "SECRET_KEY": "***" if env("SECRET_KEY") else "(默认值)",
        "DEBUG_TOKEN": "***" if env("DEBUG_TOKEN") else "(使用默认 hermes-debug-2024)",
        "_cache_backend": cache_stats().get("backend", "memory"),
    }
