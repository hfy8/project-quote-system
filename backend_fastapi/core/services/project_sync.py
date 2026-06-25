"""
项目落地状态同步服务

调用外部项目管理系统接口 (http://222.92.47.101/prod-api/project/list),
拉取所有已落地的项目 scheme_no, 缓存在内存 set 中,
供报价单列表查询/取消归档时判断使用。

特点:
- 后台定时刷新 (每 5 分钟)
- 启动时同步初始化一次 (10s 超时)
- 接口失败保留旧 set, 不影响主流程
- 多线程安全 (用 threading.Lock 保护 set 替换)
"""

import logging
import threading
import time
from typing import Optional, Set

import requests

logger = logging.getLogger(__name__)

# 外部接口配置
_PROJECT_API_URL = "http://222.92.47.101/prod-api/project/list"
_PROJECT_API_TIMEOUT = 15  # 秒
_PROJECT_REFRESH_INTERVAL = 300  # 5 分钟
_PAGE_SIZE = 200  # 外部接口默认 10/页, 但我们用 200 拉全量 (实测支持)
_INIT_TIMEOUT = 10  # 启动初始化超时


class ProjectSyncService:
    """项目落地状态同步服务 (单例)

    维护一个内存 set: scheme_no -> bool
    - True: 该 scheme_no 在外部项目系统中已落地
    - 不存在或失败: 视为 False (允许操作)
    """

    def __init__(self):
        self._lock = threading.Lock()
        self._scheme_nos: Set[str] = set()
        self._last_synced_at: Optional[float] = None
        self._last_error: Optional[str] = None
        self._stop_event = threading.Event()
        self._refresh_thread: Optional[threading.Thread] = None

    def start(self):
        """启动后台刷新线程 + 同步初始化一次"""
        # 启动时同步初始化 (快速失败, 不阻塞主流程太久)
        try:
            logger.info("[ProjectSync] 启动初始化...")
            self._refresh_sync()
            logger.info(f"[ProjectSync] 初始化完成, 当前已落地项目数: {len(self._scheme_nos)}")
        except Exception as e:
            logger.warning(f"[ProjectSync] 初始化失败 (继续启动): {e}")

        # 后台刷新线程
        if self._refresh_thread is None or not self._refresh_thread.is_alive():
            self._stop_event.clear()
            self._refresh_thread = threading.Thread(
                target=self._refresh_loop, name="project-sync-refresher", daemon=True
            )
            self._refresh_thread.start()
            logger.info(f"[ProjectSync] 后台刷新线程已启动, 间隔 {_PROJECT_REFRESH_INTERVAL}s")

    def stop(self):
        """停止后台刷新"""
        self._stop_event.set()

    def has_project(self, scheme_no: Optional[str]) -> bool:
        """判断报价单对应的项目是否已落地"""
        if not scheme_no:
            return False
        with self._lock:
            return scheme_no in self._scheme_nos

    def get_stats(self) -> dict:
        """获取同步状态 (用于调试/监控)"""
        with self._lock:
            return {
                "size": len(self._scheme_nos),
                "last_synced_at": self._last_synced_at,
                "last_error": self._last_error,
            }

    def _refresh_loop(self):
        """后台定时刷新循环"""
        while not self._stop_event.wait(_PROJECT_REFRESH_INTERVAL):
            try:
                self._refresh_sync()
            except Exception as e:
                logger.warning(f"[ProjectSync] 后台刷新失败: {e}")

    def _refresh_sync(self):
        """拉取外部接口全量项目 scheme_no, 替换内存 set"""
        all_scheme_nos: Set[str] = set()
        page = 1
        total_fetched = 0

        while True:
            payload = {
                "conditionList": [],
                "order": {"field": "createTime", "order": "desc"},
                "pageNum": page,
                "pageSize": _PAGE_SIZE,
            }
            try:
                resp = requests.post(
                    _PROJECT_API_URL,
                    json=payload,
                    timeout=_PROJECT_API_TIMEOUT,
                )
                resp.raise_for_status()
                data = resp.json()
            except Exception as e:
                raise RuntimeError(f"外部接口调用失败 (page={page}): {e}")

            if data.get("code") != 0:
                raise RuntimeError(f"外部接口返回错误 (page={page}): {data}")

            rows = data.get("data") or []
            if not rows:
                break

            for row in rows:
                sno = row.get("schemeNo")
                if sno:
                    all_scheme_nos.add(sno)
            total_fetched += len(rows)

            # 最后一页 (不足 pageSize)
            if len(rows) < _PAGE_SIZE:
                break
            page += 1

        # 替换内存 set (原子操作)
        with self._lock:
            self._scheme_nos = all_scheme_nos
            self._last_synced_at = time.time()
            self._last_error = None

        logger.info(f"[ProjectSync] 同步成功: 本次拉取 {total_fetched} 条, set 大小 {len(all_scheme_nos)}")


# 全局单例
project_sync = ProjectSyncService()
