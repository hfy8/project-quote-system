"""慢 SQL 监听器 (v17)

监听 SQLAlchemy 的 before_cursor_execute / after_cursor_execute 事件,
记录执行时间 > 阈值的 SQL 到慢查询日志 + 内存环形缓冲。

- 内存缓冲: 最近 200 条，供 AI 工具 get_slow_queries 实时查询
- 日志文件: logs/slow_queries.log（持久化 + AI 工具 grep_logs 也能查）
- 阈值: 500ms（可通过 SLOW_QUERY_THRESHOLD_MS 环境变量调整）

使用:
    from core.services.slow_query_monitor import init_slow_query_monitor
    init_slow_query_monitor(engine, threshold_ms=500)
"""
import os
import time
import logging
import threading
from collections import deque
from datetime import datetime
from typing import Optional

logger = logging.getLogger('slow_query')
logger.setLevel(logging.INFO)


class SlowQueryBuffer:
    """线程安全的慢查询环形缓冲（最近 N 条）"""
    def __init__(self, max_size: int = 200):
        self._buffer = deque(maxlen=max_size)
        self._lock = threading.Lock()
        self._total_count = 0  # 总计慢查询数（启动以来）

    def add(self, record: dict):
        with self._lock:
            self._buffer.append(record)
            self._total_count += 1

    def get_recent(self, limit: int = 20, min_ms: Optional[float] = None) -> list:
        """获取最近的慢查询记录"""
        with self._lock:
            items = list(self._buffer)
        if min_ms is not None:
            items = [r for r in items if r['duration_ms'] >= min_ms]
        return items[-limit:][::-1]  # 倒序，最新在前

    def get_stats(self) -> dict:
        """慢查询统计"""
        with self._lock:
            items = list(self._buffer)
        if not items:
            return {
                'total_recent': 0,
                'total_since_start': self._total_count,
                'avg_ms': 0, 'max_ms': 0, 'p95_ms': 0,
            }
        durations = sorted([r['duration_ms'] for r in items])
        n = len(durations)
        return {
            'total_recent': n,
            'total_since_start': self._total_count,
            'avg_ms': round(sum(durations) / n, 1),
            'max_ms': round(durations[-1], 1),
            'p95_ms': round(durations[int(n * 0.95)] if n > 1 else durations[-1], 1),
        }

    def clear(self):
        with self._lock:
            self._buffer.clear()


# 全局实例（AI 工具直接 import 用）
slow_query_buffer = SlowQueryBuffer(max_size=200)


def _setup_file_logger(log_dir: str = 'logs') -> logging.FileHandler:
    """配置慢查询文件 logger"""
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, 'slow_queries.log')
    handler = logging.FileHandler(log_file, encoding='utf-8')
    handler.setFormatter(logging.Formatter(
        '%(asctime)s.%(msecs)03d [SLOW_SQL] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    ))
    # 避免重复添加 handler
    if not any(isinstance(h, logging.FileHandler) and h.baseFilename == handler.baseFilename
               for h in logger.handlers):
        logger.addHandler(handler)
    return handler


def init_slow_query_monitor(engine, threshold_ms: int = None):
    """注册 SQLAlchemy 事件，开始监听慢查询

    Args:
        engine: SQLAlchemy Engine
        threshold_ms: 阈值（毫秒），默认从环境变量读，默认 500
    """
    from sqlalchemy import event

    threshold = threshold_ms or int(os.getenv('SLOW_QUERY_THRESHOLD_MS', '500'))
    _setup_file_logger()

    @event.listens_for(engine, 'before_cursor_execute')
    def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        # 存开始时间到 context
        context._slow_query_start = time.time()

    @event.listens_for(engine, 'after_cursor_execute')
    def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        start = getattr(context, '_slow_query_start', None)
        if start is None:
            return
        duration_ms = (time.time() - start) * 1000
        if duration_ms < threshold:
            return

        # 截断 SQL（避免超长 + JSON 序列化报错）
        sql_short = ' '.join(statement.split())[:500]
        record = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'duration_ms': round(duration_ms, 2),
            'sql': sql_short,
            'params': str(parameters)[:200] if parameters else None,
        }

        # 1. 写文件
        logger.warning(
            f'{duration_ms:.1f}ms | {sql_short[:200]}'
        )

        # 2. 内存缓冲（AI 工具读）
        slow_query_buffer.add(record)

        # 3. 极端慢（>3s）输出到 stderr，触发告警
        if duration_ms > 3000:
            import sys
            print(f'\n🚨 SLOW_SQL {duration_ms:.0f}ms: {sql_short[:100]}\n', file=sys.stderr)

    logger.info(f'✅ 慢 SQL 监听已启动 (阈值 {threshold}ms)')
    return threshold
