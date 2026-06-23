"""
debug cache stats endpoint
"""
import os
from fastapi import APIRouter, HTTPException, Header
from core.services.cache import cache_stats, _memory

router = APIRouter(prefix="/api/_debug", tags=["debug"])
# 优先从环境变量 DEBUG_TOKEN 读, 默认值 (生产请覆盖)
TOKEN = os.environ.get("DEBUG_TOKEN", "hermes-debug-2024")


@router.get("/cache-stats")
def get_cache_stats(x_debug_token: str = Header(None)):
    if x_debug_token != TOKEN:
        raise HTTPException(status_code=403, detail="forbidden")

    stats = cache_stats()
    stats["_memory_keys"] = list(_memory._data.keys())[:20] if hasattr(_memory, "_data") else []
    stats["_memory_size"] = len(_memory._data) if hasattr(_memory, "_data") else 0
    stats["_memory_max"] = getattr(_memory, "_max_size", None)
    return stats
