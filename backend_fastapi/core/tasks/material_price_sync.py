"""原材料价格同步任务 - 定时通过品号从外部 API 同步最新价格

流程:
  1) 查 materials WHERE item_no IS NOT NULL (有品号的物料)
  2) 调用外部价格 API, 传入 item_no, 拿到最新 unit_price
  3) 写入 materials.unit_price + last_price_synced_at + last_price_sync_status

外部 API 形态 (示例, 可由环境变量配置):
  GET {MATERIAL_PRICE_API_URL}?item_no=XXX
  Headers: Authorization: Bearer {MATERIAL_PRICE_API_KEY}
  Response:
    {
      "item_no": "MAT-001",
      "unit_price": 99.50,
      "currency": "CNY",
      "synced_at": "2026-07-01T12:00:00Z"
    }

mock 模式 (默认, 当 MATERIAL_PRICE_API_URL 未配置):
  按 item_no 哈希生成稳定的 mock 价格, 便于本地测试和验证逻辑

防错设计:
  - 单条失败 → 跳过该条 + 记录 error, 不中断整批
  - 外部 API 超时 → 重试 3 次 (指数退避)
  - 价格变化幅度 > 50% → 标记 warning (避免 API 异常导致报价大面积错误)
"""
import logging
import os
import hashlib
from datetime import datetime
from typing import Optional

import requests

from db import db_session_factory
from core.models.material import Material

logger = logging.getLogger(__name__)

# 外部 API 配置 (从环境变量读取, 默认 mock 模式)
EXTERNAL_API_URL = os.environ.get("MATERIAL_PRICE_API_URL", "").strip()  # 空 → mock 模式
EXTERNAL_API_KEY = os.environ.get("MATERIAL_PRICE_API_KEY", "").strip()
EXTERNAL_TIMEOUT = int(os.environ.get("MATERIAL_PRICE_API_TIMEOUT", "10"))
SOURCE_NAME = "external-api" if EXTERNAL_API_URL else "mock-api"

# 重试配置
MAX_RETRIES = 3
RETRY_BACKOFF_BASE = 2  # 秒

# 价格波动报警阈值 (相对原价格)
PRICE_CHANGE_ALERT_THRESHOLD = 0.5  # 50%


def _fetch_price_from_external(item_no: str) -> Optional[dict]:
    """从外部 API 拉取单个品号的价格

    返回 dict {item_no, unit_price, currency, synced_at} 或 None (失败)
    mock 模式: 按 item_no 哈希生成稳定价格
    """
    if not EXTERNAL_API_URL:
        # mock 模式: 哈希 → 价格 (10-500 之间, 稳定)
        h = hashlib.md5(item_no.encode("utf-8")).hexdigest()
        price = 10 + (int(h[:6], 16) % 490) + round(int(h[6:8], 16) / 255, 2)
        return {
            "item_no": item_no,
            "unit_price": round(price, 2),
            "currency": "CNY",
            "synced_at": datetime.utcnow().isoformat() + "Z",
            "_mock": True,
        }

    # 真实 API 模式
    url = f"{EXTERNAL_API_URL.rstrip('/')}?item_no={item_no}"
    headers = {}
    if EXTERNAL_API_KEY:
        headers["Authorization"] = f"Bearer {EXTERNAL_API_KEY}"

    last_err: Optional[Exception] = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.get(url, headers=headers, timeout=EXTERNAL_TIMEOUT)
            resp.raise_for_status()
            data = resp.json()
            # 容错: 字段名不一致
            return {
                "item_no": data.get("item_no") or item_no,
                "unit_price": float(data.get("unit_price") or data.get("price") or 0),
                "currency": data.get("currency", "CNY"),
                "synced_at": data.get("synced_at") or datetime.utcnow().isoformat() + "Z",
            }
        except (requests.RequestException, ValueError, KeyError) as e:
            last_err = e
            logger.warning(f"[{item_no}] attempt {attempt}/{MAX_RETRIES} failed: {e}")
            if attempt < MAX_RETRIES:
                import time
                time.sleep(RETRY_BACKOFF_BASE ** attempt)

    logger.error(f"[{item_no}] all {MAX_RETRIES} retries failed: {last_err}")
    return None


def sync_material_prices(batch_size: int = 50, dry_run: bool = False) -> dict:
    """同步所有有品号物料的最新价格

    Args:
        batch_size: 每批 commit 一次的物料数 (避免单次事务过大)
        dry_run: True 时只统计不写库

    Returns:
        dict {total, updated, unchanged, failed, skipped, source, started_at, finished_at, duration_s}
    """
    started_at = datetime.utcnow()
    session = db_session_factory()
    try:
        # 1) 查所有有品号 + active 状态的物料
        candidates = session.query(Material).filter(
            Material.item_no.isnot(None),
            Material.item_no != "",
            Material.status == "active",
        ).order_by(Material.id).all()

        total = len(candidates)
        logger.info(f"📦 Found {total} materials with item_no, source={SOURCE_NAME}, dry_run={dry_run}")

        updated = 0
        unchanged = 0
        failed = 0
        skipped = 0
        warnings: list[str] = []

        # 2) 逐个同步 (单条失败不中断)
        for i, mat in enumerate(candidates, 1):
            try:
                result = _fetch_price_from_external(mat.item_no)
                if not result:
                    # 同步失败 → 记录但不抛
                    if not dry_run:
                        mat.last_price_synced_at = datetime.utcnow()
                        mat.last_price_sync_status = "failed"
                        mat.last_price_sync_error = "external api returned None (after retries)"
                        mat.last_price_sync_source = SOURCE_NAME
                    failed += 1
                    continue

                new_price = float(result.get("unit_price", 0))
                old_price = float(mat.unit_price) if mat.unit_price else 0.0

                # 价格波动报警
                if old_price > 0:
                    change_ratio = abs(new_price - old_price) / old_price
                    if change_ratio > PRICE_CHANGE_ALERT_THRESHOLD:
                        warn_msg = (
                            f"[{mat.item_no}] {mat.name}: price changed "
                            f"{old_price:.2f} → {new_price:.2f} ({change_ratio*100:.1f}%)"
                        )
                        logger.warning(f"⚠️ {warn_msg}")
                        warnings.append(warn_msg)

                if not dry_run:
                    if abs(new_price - old_price) > 0.001:
                        mat.unit_price = new_price
                        updated += 1
                    else:
                        unchanged += 1
                    mat.last_price_synced_at = datetime.utcnow()
                    mat.last_price_sync_status = "success"
                    mat.last_price_sync_error = None
                    mat.last_price_sync_source = SOURCE_NAME

                # 批量 commit, 避免大事务
                if not dry_run and i % batch_size == 0:
                    session.commit()
                    logger.info(f"  progress: {i}/{total} processed (updated={updated}, unchanged={unchanged}, failed={failed})")

            except Exception as e:
                logger.exception(f"[{mat.item_no}] unexpected error: {e}")
                if not dry_run:
                    try:
                        mat.last_price_synced_at = datetime.utcnow()
                        mat.last_price_sync_status = "failed"
                        mat.last_price_sync_error = str(e)[:500]
                        mat.last_price_sync_source = SOURCE_NAME
                    except Exception:
                        pass
                failed += 1

        if not dry_run:
            session.commit()

        finished_at = datetime.utcnow()
        duration = (finished_at - started_at).total_seconds()

        result = {
            "source": SOURCE_NAME,
            "dry_run": dry_run,
            "total": total,
            "updated": updated,
            "unchanged": unchanged,
            "failed": failed,
            "skipped": skipped,
            "warnings": warnings[:10],  # 最多 10 条
            "warning_count": len(warnings),
            "started_at": started_at.isoformat() + "Z",
            "finished_at": finished_at.isoformat() + "Z",
            "duration_s": round(duration, 2),
        }
        logger.info(f"✅ Material price sync done: {result}")
        return result

    except Exception as e:
        session.rollback()
        logger.exception(f"Material price sync crashed: {e}")
        return {"error": f"同步失败: {str(e)}"}
    finally:
        session.close()


# APScheduler 调度的入口函数 (包装, 防异常影响 scheduler)
def scheduled_sync_material_prices():
    """定时任务入口: 同步原材料价格 (apscheduler 调用)"""
    try:
        result = sync_material_prices(dry_run=False)
        logger.info(f"Scheduled material price sync result: {result}")
        return result
    except Exception as e:
        logger.exception(f"Scheduled material price sync crashed: {e}")