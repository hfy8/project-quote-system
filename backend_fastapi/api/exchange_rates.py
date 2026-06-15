"""FastAPI 路由 - Exchange Rates (迁移版)"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from core.models.exchange_rate import ExchangeRate
from core.auth import get_db, get_current_user_id

router = APIRouter(prefix='/api/exchange_rates')


@router.get('/base')
def get_base_currency(db=Depends(get_db)):
    """获取基准货币"""
    base = db.query(ExchangeRate).filter_by(is_base=True).first()
    if not base:
        return {'currency': 'CNY', 'rate': 1.0, 'is_base': True}
    return base.to_dict()


class ExchangeRateCreate(BaseModel):
    currency: str
    rate: float = 1.0
    is_base: bool = False
    description: Optional[str] = None


class ExchangeRateUpdate(BaseModel):
    rate: Optional[float] = None
    is_base: Optional[bool] = None
    description: Optional[str] = None


def _set_base_currency(db, currency: str, rate_value: float, user_id: str, exclude_id: Optional[int] = None):
    """内部：设置指定货币为基准货币，重新计算所有汇率"""
    from utils.logger import log_operation

    old_base = db.query(ExchangeRate).filter_by(is_base=True).first()

    # 取消所有现有基准
    base_query = db.query(ExchangeRate).filter_by(is_base=True)
    if exclude_id is not None:
        base_query = base_query.filter(ExchangeRate.id != exclude_id)
    base_query.update({'is_base': False})

    # 如果旧基准存在且不同于新基准，计算比例更新所有汇率
    if old_base and old_base.currency != currency:
        old_rate_value = old_base.rate
        for r in db.query(ExchangeRate).filter(ExchangeRate.currency != currency).all():
            r.rate = round(r.rate / old_rate_value * rate_value, 6)

    db.commit()
    log_operation(user_id, 'update', 'exchange_rate', f'设置基准货币为 "{currency}"')


# ---- 端点 ----

@router.get('')
def list_exchange_rates(db=Depends(get_db)):
    """列出所有汇率配置"""
    rates = db.query(ExchangeRate).all()
    return JSONResponse(content={"items": [r.to_dict() for r in rates]})


@router.post('', status_code=201)
def create_exchange_rate(body: ExchangeRateCreate, db=Depends(get_db), user_id: str = Depends(get_current_user_id)):
    """创建汇率配置"""
    from utils.logger import log_operation

    if body.is_base:
        # 重新计算所有汇率：以新基准货币的汇率为基准
        _set_base_currency(db, body.currency, body.rate, user_id)
        rate = ExchangeRate(
            currency=body.currency,
            rate=1.0,  # 基准货币固定为1
            is_base=True,
            description=body.description,
        )
        db.add(rate)
        db.commit()
        log_operation(user_id, 'create', 'exchange_rate', f'设置基准货币 "{body.currency}"')
        return JSONResponse(content=rate.to_dict(), status_code=201)

    rate = ExchangeRate(
        currency=body.currency,
        rate=body.rate,
        is_base=False,
        description=body.description,
    )
    db.add(rate)
    db.commit()
    log_operation(user_id, 'create', 'exchange_rate', f'创建汇率 "{body.currency}"={body.rate}')
    return JSONResponse(content=rate.to_dict(), status_code=201)


@router.post('/{rate_id}/set-base')
def set_base_currency(rate_id: int, db=Depends(get_db), user_id: str = Depends(get_current_user_id)):
    """设置基准货币（前端专用接口，相当于 is_base=True）"""
    from utils.logger import log_operation

    rate = db.query(ExchangeRate).get(rate_id)
    if not rate:
        raise HTTPException(status_code=404, detail="汇率不存在")

    _set_base_currency(db, rate.currency, rate.rate, user_id, exclude_id=rate_id)
    rate.is_base = True
    rate.rate = 1.0  # 基准货币固定为1
    db.commit()
    log_operation(user_id, 'update', 'exchange_rate', f'设置基准货币为 "{rate.currency}"')
    return JSONResponse(content=rate.to_dict())


@router.put('/{rate_id}')
def update_exchange_rate(rate_id: int, body: ExchangeRateUpdate, db=Depends(get_db), user_id: str = Depends(get_current_user_id)):
    """更新汇率配置"""
    from utils.logger import log_operation

    rate = db.query(ExchangeRate).get(rate_id)
    if not rate:
        raise HTTPException(status_code=404, detail="汇率不存在")

    # 如果设置为基准货币
    if body.is_base and not rate.is_base:
        _set_base_currency(db, rate.currency, body.rate or rate.rate, user_id, exclude_id=rate_id)
        rate.is_base = True
        rate.rate = 1.0  # 基准货币固定为1
        db.commit()
        log_operation(user_id, 'update', 'exchange_rate', f'设置基准货币为 "{rate.currency}"')
        return JSONResponse(content=rate.to_dict())

    # 普通更新
    data = body.model_dump(exclude_unset=True)
    for key in ("rate", "description"):
        if key in data:
            setattr(rate, key, data[key])
    db.commit()
    return JSONResponse(content=rate.to_dict())


@router.delete('/{rate_id}')
def delete_exchange_rate(rate_id: int, db=Depends(get_db), user_id: str = Depends(get_current_user_id)):
    """删除汇率配置"""
    from utils.logger import log_operation

    rate = db.query(ExchangeRate).get(rate_id)
    if not rate:
        raise HTTPException(status_code=404, detail="汇率不存在")
    db.delete(rate)
    db.commit()
    log_operation(user_id, 'delete', 'exchange_rate', f'删除汇率 "{rate.currency}"')
    return JSONResponse(content={"message": "删除成功"})


@router.get('/convert')
def convert_currency(
    from_currency: str = Query('CNY', alias='from'),
    to_currency: str = Query('CNY', alias='to'),
    amount: float = Query(0.0),
    db=Depends(get_db),
):
    """货币转换"""
    from_rate = db.query(ExchangeRate).filter_by(currency=from_currency).first()
    to_rate = db.query(ExchangeRate).filter_by(currency=to_currency).first()

    if not from_rate or not to_rate:
        raise HTTPException(status_code=400, detail="货币代码不存在")

    # 转换为基准货币，再转换为目标货币
    base_amount = amount / from_rate.rate
    result = base_amount * to_rate.rate

    return JSONResponse(content={
        'from': from_currency,
        'to': to_currency,
        'amount': amount,
        'result': round(result, 2),
        'rate': round(to_rate.rate / from_rate.rate, 4),
    })
