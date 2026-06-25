"""汇率同步任务 - 从 exchangerate-api.com 同步汇率到 exchange_rates 表

外部接口: https://open.er-api.com/v6/latest/{BASE}
- 返回: 1 BASE = X 其它货币
- 字段: rates: {CCY: rate}

本地表 exchange_rates:
- 字段: currency, rate (1 单位本币 = X 基准币), is_base, description
- 基准 (is_base=true): rate 固定为 1.0
- 非基准: rate 表示"1 单位此币 = X CNY"

转换公式:
    local_rate[CCY] = 1 / external_rate[CCY]   (CCY != BASE)
    local_rate[BASE] = 1.0
"""
import logging
from datetime import datetime

import requests

from db import db_session_factory
from core.models.exchange_rate import ExchangeRate

logger = logging.getLogger(__name__)

# 外部接口配置
EXTERNAL_API_URL = "https://open.er-api.com/v6/latest/{base}"
EXTERNAL_TIMEOUT = 10  # 秒

# 外部 CCY -> 本地 CCY 别名映射 (API 偶尔用非标准码)
CCY_ALIAS = {
    "CNH": "CNH",  # 离岸人民币, 我们的系统没有, 跳过
}


def _fetch_external_rates(base_ccy: str = "CNY") -> dict:
    """从外部接口拉取汇率

    返回 dict[ccy, rate] (1 BASE = rate CCY)
    失败抛 requests.RequestException
    """
    url = EXTERNAL_API_URL.format(base=base_ccy)
    logger.info(f"Fetching exchange rates from {url}")
    resp = requests.get(url, timeout=EXTERNAL_TIMEOUT)
    resp.raise_for_status()
    data = resp.json()

    if data.get("result") != "success":
        raise ValueError(f"External API returned non-success: {data.get('result')}")

    rates = data.get("rates", {})
    if not rates:
        raise ValueError("External API returned empty rates")

    logger.info(f"Got {len(rates)} rates from external API, base={data.get('base_code')}")
    return rates


def sync_exchange_rates(base_ccy: str = "CNY", create_missing: bool = True) -> dict:
    """同步汇率到本地 exchange_rates 表

    Args:
        base_ccy: 基准货币代码 (默认 CNY), 必须与本地表 is_base=true 的货币一致
        create_missing: 表中没有的币种是否新增 (True=补全, False=只更新已存在)

    Returns:
        dict {updated, created, skipped, total_external, base_ccy, synced_at}
    """
    session = db_session_factory()
    try:
        # 1) 校验本地基准货币
        base_record = session.query(ExchangeRate).filter_by(is_base=True).first()
        if not base_record:
            logger.warning("No base currency found in exchange_rates, skipping sync")
            return {"error": "本地未配置基准货币"}
        if base_record.currency != base_ccy:
            logger.warning(
                f"Local base currency ({base_record.currency}) != requested ({base_ccy}), "
                f"using local base"
            )
            base_ccy = base_record.currency

        # 2) 拉外部数据
        external_rates = _fetch_external_rates(base_ccy)

        # 3) 拉本地现有记录
        local_records = {
            r.currency: r
            for r in session.query(ExchangeRate).all()
        }

        updated = 0
        created = 0
        skipped = 0

        # 4) 遍历外部汇率, 写入本地
        for ccy, ext_rate in external_rates.items():
            # 跳过离岸人民币等 (我们没有)
            if ccy in CCY_ALIAS and CCY_ALIAS[ccy] is None:
                skipped += 1
                continue

            # 计算本地汇率: 1 本币 = X 基准币
            # external: 1 BASE = ext_rate CCY => 1 CCY = 1/ext_rate BASE
            if ccy == base_ccy:
                local_rate = 1.0
            elif ext_rate and ext_rate > 0:
                local_rate = round(1.0 / ext_rate, 6)
            else:
                logger.warning(f"Invalid rate for {ccy}: {ext_rate}, skipping")
                skipped += 1
                continue

            if ccy in local_records:
                # 更新现有
                r = local_records[ccy]
                if r.is_base:
                    # 基准货币保持 1.0
                    r.rate = 1.0
                else:
                    r.rate = local_rate
                r.description = r.description or f"{ccy}汇率 (同步自 er-api.com)"
                r.updated_at = datetime.utcnow()
                updated += 1
            elif create_missing:
                # 新增
                r = ExchangeRate(
                    currency=ccy,
                    rate=local_rate,
                    is_base=False,
                    description=f"{ccy}汇率 (同步自 er-api.com)",
                )
                session.add(r)
                created += 1
            else:
                skipped += 1

        session.commit()
        result = {
            "base_ccy": base_ccy,
            "synced_at": datetime.utcnow().isoformat(),
            "total_external": len(external_rates),
            "updated": updated,
            "created": created,
            "skipped": skipped,
        }
        logger.info(f"Exchange rate sync complete: {result}")
        return result

    except requests.RequestException as e:
        session.rollback()
        logger.error(f"External API request failed: {e}")
        return {"error": f"外部接口调用失败: {str(e)}"}
    except Exception as e:
        session.rollback()
        logger.exception(f"Exchange rate sync failed: {e}")
        return {"error": f"同步失败: {str(e)}"}
    finally:
        session.close()


# APScheduler 调度的入口函数 (包装, 防异常影响 scheduler)
def scheduled_sync_exchange_rates():
    """定时任务入口: 同步汇率 (apscheduler 调用)"""
    try:
        result = sync_exchange_rates(base_ccy="CNY", create_missing=True)
        logger.info(f"Scheduled exchange rate sync result: {result}")
        return result
    except Exception as e:
        logger.exception(f"Scheduled exchange rate sync crashed: {e}")
