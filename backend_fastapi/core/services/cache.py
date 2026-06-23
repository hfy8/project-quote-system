"""Redis 缓存模块 (v17)

设计目标：
- 有 Redis 用 Redis（快），没 Redis 自动退化到内存（不挂）
- 所有缓存 key 加 namespace 前缀，避免冲突
- 写操作时主动失效对应 key
- 支持 TTL（默认 30s）
- 启动时探测 Redis，不可用就 warn

用法:
    from core.services.cache import cache_get, cache_set, cache_invalidate

    val = cache_get('quotations:list:page=1')
    if val is None:
        val = expensive_query()
        cache_set('quotations:list:page=1', val, ttl=30)
"""
import os
import json
import time
import logging
import threading
from collections import OrderedDict
from typing import Any, Optional

logger = logging.getLogger('cache')

# ============== 配置 ==============
REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
CACHE_NAMESPACE = os.environ.get('CACHE_NAMESPACE', 'pqs')
CACHE_DEFAULT_TTL = int(os.environ.get('CACHE_DEFAULT_TTL', '30'))
CACHE_DISABLED = os.environ.get('CACHE_DISABLED', 'false').lower() == 'true'

# ============== 内存 LRU 兜底 ==============
class _MemoryLRU:
    """线程安全的内存 LRU 缓存（兜底用）"""
    def __init__(self, max_size: int = 1000):
        self._data = OrderedDict()
        self._lock = threading.Lock()
        self._max = max_size
        self._hits = 0
        self._misses = 0

    def get(self, key: str) -> Optional[Any]:
        with self._lock:
            if key in self._data:
                self._data.move_to_end(key)
                self._hits += 1
                return self._data[key]
        self._misses += 1
        return None

    def set(self, key: str, value: Any):
        with self._lock:
            if key in self._data:
                self._data.move_to_end(key)
            self._data[key] = value
            if len(self._data) > self._max:
                self._data.popitem(last=False)

    def delete(self, key: str):
        with self._lock:
            self._data.pop(key, None)

    def delete_prefix(self, prefix: str) -> int:
        cnt = 0
        with self._lock:
            keys = [k for k in self._data if k.startswith(prefix)]
            for k in keys:
                self._data.pop(k, None)
                cnt += 1
        return cnt

    def clear(self):
        with self._lock:
            self._data.clear()

    def stats(self) -> dict:
        total = self._hits + self._misses
        return {
            'backend': 'memory',
            'size': len(self._data),
            'max': self._max,
            'hits': self._hits,
            'misses': self._misses,
            'hit_rate': round(self._hits / total * 100, 1) if total > 0 else 0,
        }


_memory = _MemoryLRU(max_size=1000)
_redis_client = None
_backend = 'disabled'  # disabled | memory | redis


def _connect_redis():
    """尝试连接 Redis（启动时调用）"""
    global _redis_client, _backend
    if CACHE_DISABLED:
        logger.info('缓存已禁用 (CACHE_DISABLED=true)')
        _backend = 'disabled'
        return
    try:
        import redis
        client = redis.Redis.from_url(REDIS_URL, decode_responses=True, socket_timeout=2)
        client.ping()
        _redis_client = client
        _backend = 'redis'
        logger.info(f'✅ Redis 缓存已连接: {REDIS_URL} (namespace={CACHE_NAMESPACE})')
    except Exception as e:
        _backend = 'memory'
        logger.warning(f'⚠️ Redis 不可用 ({e.__class__.__name__}: {e}), 退化到内存缓存')


def _k(key: str) -> str:
    """加 namespace 前缀"""
    return f'{CACHE_NAMESPACE}:{key}'


def cache_get(key: str) -> Optional[Any]:
    """获取缓存值；未命中返回 None"""
    if _backend == 'disabled':
        return None
    k = _k(key)
    if _backend == 'redis':
        try:
            v = _redis_client.get(k)
            if v is None:
                return None
            return json.loads(v)
        except Exception as e:
            logger.warning(f'cache_get 异常: {e}')
            return None
    return _memory.get(k)


def cache_set(key: str, value: Any, ttl: int = None) -> bool:
    """设置缓存值（默认 TTL 30s）"""
    if _backend == 'disabled':
        return False
    k = _k(key)
    ttl = ttl or CACHE_DEFAULT_TTL
    if _backend == 'redis':
        try:
            _redis_client.setex(k, ttl, json.dumps(value, ensure_ascii=False, default=str))
            return True
        except Exception as e:
            logger.warning(f'cache_set 异常: {e}')
            return False
    _memory.set(k, value)
    return True


def cache_invalidate(key: str) -> bool:
    """失效单个 key"""
    if _backend == 'disabled':
        return False
    k = _k(key)
    if _backend == 'redis':
        try:
            _redis_client.delete(k)
            return True
        except Exception:
            return False
    _memory.delete(k)
    return True


def cache_invalidate_prefix(prefix: str) -> int:
    """失效所有以 prefix 开头的 key（用于"任何写操作清掉整个列表缓存"）"""
    if _backend == 'disabled':
        return 0
    if _backend == 'redis':
        try:
            full_prefix = _k(prefix)
            # SCAN 而不是 KEYS（避免阻塞）
            count = 0
            for k in _redis_client.scan_iter(match=full_prefix + '*', count=100):
                _redis_client.delete(k)
                count += 1
            return count
        except Exception as e:
            logger.warning(f'cache_invalidate_prefix 异常: {e}')
            return 0
    return _memory.delete_prefix(_k(prefix))


def cache_stats() -> dict:
    """缓存统计（调试用）"""
    if _backend == 'redis':
        try:
            info = _redis_client.info('stats')
            return {
                'backend': 'redis',
                'url': REDIS_URL,
                'namespace': CACHE_NAMESPACE,
                'redis_hits': info.get('keyspace_hits', 0),
                'redis_misses': info.get('keyspace_misses', 0),
            }
        except Exception:
            pass
    return _memory.stats()


def get_backend() -> str:
    """获取当前后端: 'redis' | 'memory' | 'disabled'"""
    return _backend


# 启动时连接（模块 import 即生效）
_connect_redis()
