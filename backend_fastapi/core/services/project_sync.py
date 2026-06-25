"""项目落地状态同步服务 (v2 - DB 持久化版)

数据流:
- 外部 project/list → 全量 UPSERT 到 DB (landing_projects)
- 启动时加载 scheme_no 集合到内存 cache
- 每 30 分钟刷新一次 DB
- 列表查询: 优先用内存 cache, 命中失败回退 DB

特点:
- DB 落地, 重启无感
- 内存 cache 加速查询 (O(1))
- 增量字段扩展 (full_data JSONB)
- 预留 webhook 接口 (实时同步, 待实现)
"""

import logging
import threading
import time
from typing import Optional, Set

import requests

logger = logging.getLogger(__name__)

# 外部接口配置
_PROJECT_API_URL = "http://222.92.47.101/prod-api/project/list"
_PROJECT_API_TIMEOUT = 30  # 秒
_PROJECT_REFRESH_INTERVAL = 1800  # 30 分钟
_PAGE_SIZE = 500


class ProjectSyncService:
    """项目落地状态同步服务 (DB 版, 单例)

    内存 cache: Set[str] scheme_no
    持久化: DB landing_projects 表
    """

    def __init__(self):
        self._lock = threading.Lock()
        self._scheme_nos: Set[str] = set()
        self._cache_loaded_at: Optional[float] = None
        self._last_db_sync_at: Optional[float] = None
        self._last_db_sync_count: int = 0
        self._last_error: Optional[str] = None
        self._stop_event = threading.Event()
        self._refresh_thread: Optional[threading.Thread] = None

    # ===== 公共 API =====

    def has_project(self, scheme_no: Optional[str]) -> bool:
        """判断报价单对应的项目是否已落地 (O(1), 内存查)"""
        if not scheme_no:
            return False
        with self._lock:
            return scheme_no in self._scheme_nos

    def get_stats(self) -> dict:
        return {
            "cache_size": len(self._scheme_nos),
            "cache_loaded_at": self._cache_loaded_at,
            "last_db_sync_at": self._last_db_sync_at,
            "last_db_sync_count": self._last_db_sync_count,
            "last_error": self._last_error,
        }

    def start(self):
        """启动: 加载 cache + 启动后台刷新线程 + 首次 DB 同步"""
        # 先加载 cache (从 DB, 启动几乎瞬时)
        try:
            self._load_cache_from_db()
        except Exception as e:
            logger.warning(f"[ProjectSync] 启动时 cache 加载失败: {e}")

        # 后台线程: 首次同步 + 定时刷新
        if self._refresh_thread is None or not self._refresh_thread.is_alive():
            self._stop_event.clear()
            self._refresh_thread = threading.Thread(
                target=self._refresh_loop, name="project-sync-refresher", daemon=True
            )
            self._refresh_thread.start()
            logger.info(f"[ProjectSync] 后台刷新线程已启动, 间隔 {_PROJECT_REFRESH_INTERVAL}s")

    def stop(self):
        self._stop_event.set()

    def reload_cache(self):
        """手动重新加载 cache (例如 webhook 实时更新后)"""
        self._load_cache_from_db()

    # ===== 内部 =====

    def _load_cache_from_db(self):
        """从 DB 加载所有 scheme_no 到内存 cache"""
        from db import db_session_factory
        from core.models.landing_project import LandingProject
        session = db_session_factory()
        try:
            rows = session.query(LandingProject.scheme_no).all()
            new_set = {row[0] for row in rows if row[0]}
            with self._lock:
                self._scheme_nos = new_set
                self._cache_loaded_at = time.time()
            logger.info(f"[ProjectSync] cache 从 DB 加载完成: {len(new_set)} 条")
        finally:
            session.close()

    def _refresh_loop(self):
        """后台首次同步 + 定时刷新"""
        # 首次同步 (立即)
        try:
            self._sync_db()
            self._load_cache_from_db()
        except Exception as e:
            logger.warning(f"[ProjectSync] 首次 DB 同步失败 (继续运行): {e}")

        # 定时刷新
        while not self._stop_event.wait(_PROJECT_REFRESH_INTERVAL):
            try:
                self._sync_db()
                self._load_cache_from_db()
            except Exception as e:
                logger.warning(f"[ProjectSync] 定时 DB 同步失败: {e}")

    def _sync_db(self):
        """全量拉取外部接口 + UPSERT 到 DB"""
        all_rows = []
        page = 1

        while True:
            payload = {
                "conditionList": [],
                "order": {"field": "createTime", "order": "desc"},
                "pageNum": page,
                "pageSize": _PAGE_SIZE,
            }
            resp = requests.post(
                _PROJECT_API_URL, json=payload, timeout=_PROJECT_API_TIMEOUT
            )
            resp.raise_for_status()
            data = resp.json()
            if data.get("code") != 0:
                raise RuntimeError(f"外部接口错误 (page={page}): {data}")

            rows = data.get("data") or []
            if not rows:
                break

            for r in rows:
                sno = r.get("schemeNo")
                if not sno:
                    continue
                all_rows.append({
                    "scheme_no": sno,
                    "external_project_id": str(r.get("projectId", "")) or None,
                    "scheme_name": r.get("schemeName"),
                    "customer_name": r.get("customerName"),
                    "project_manager_name": r.get("projectManagerName"),
                    "project_status": r.get("projectStatus"),
                    "archive_status": bool(r.get("archiveStatus", False)),
                    "full_data": r,
                    "last_synced_at": datetime.utcnow(),
                    "first_synced_at": datetime.utcnow(),  # UPSERT 用 ON CONFLICT DO NOTHING 时不会覆盖
                })

            if len(rows) < _PAGE_SIZE:
                break
            page += 1

        if not all_rows:
            logger.info("[ProjectSync] 外部接口无数据")
            return

        # 去重: 外部接口可能返回重复 scheme_no (如 L104229 多个子项)
        # 用 last_synced_at 最大的版本
        from collections import OrderedDict
        deduped = OrderedDict()
        for r in all_rows:
            sno = r["scheme_no"]
            if sno not in deduped or r["last_synced_at"] > deduped[sno]["last_synced_at"]:
                deduped[sno] = r
        unique_rows = list(deduped.values())

        # UPSERT 到 DB (逐条 ORM merge, 避免 ON CONFLICT DO UPDATE 重复 conflict target 错误)
        from db import db_session_factory
        from core.models.landing_project import LandingProject
        from sqlalchemy import select
        session = db_session_factory()
        try:
            inserted_count = 0
            updated_count = 0
            for row in unique_rows:
                # 查是否已存在
                existing = session.query(LandingProject).filter_by(scheme_no=row["scheme_no"]).first()
                if existing:
                    # 更新 (保留 first_synced_at)
                    for k, v in row.items():
                        if k != "first_synced_at":
                            setattr(existing, k, v)
                    updated_count += 1
                else:
                    # 新增
                    obj = LandingProject(**row)
                    session.add(obj)
                    inserted_count += 1

                # 每 100 条 flush 一次, 避免长事务
                if (inserted_count + updated_count) % 100 == 0:
                    session.flush()

            session.commit()

            with self._lock:
                self._last_db_sync_at = time.time()
                self._last_db_sync_count = len(unique_rows)
                self._last_error = None

            logger.info(
                f"[ProjectSync] DB 同步成功: 总 {len(all_rows)} 条, "
                f"去重后 {len(unique_rows)} 条 (新增 {inserted_count}, 更新 {updated_count})"
            )
        except Exception as e:
            session.rollback()
            with self._lock:
                self._last_error = str(e)
            raise
        finally:
            session.close()


# 全局单例
project_sync = ProjectSyncService()


# 避免循环 import
from datetime import datetime
