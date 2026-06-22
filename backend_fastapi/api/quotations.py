"""FastAPI 路由 - Quotations (迁移版)

业务逻辑 1:1 复刻 backend/app/routes/quotations.py

路径映射 (Flask quotation_bp 注册到 /api 蓝本):
- GET    /quotations                                   → 列表
- POST   /quotations                                   → 创建
- GET    /quotations/{id}                              → 详情
- GET    /quotations/{id}/permissions                  → 权限
- PUT    /quotations/{id}                              → 更新
- DELETE /quotations/{id}                              → 删除
- PUT    /quotations/{id}/status                       → 状态更新
- GET    /quotations/{id}/versions                     → 版本列表
- GET    /quotations/{id}/versions/{version_no}        → 版本详情
- POST   /quotations/{id}/archive                      → 归档
- POST   /quotations/{id}/unarchive                    → 撤销归档
- GET    /quotations/{id}/participants                 → 参与人列表
- POST   /quotations/{id}/participants                 → 添加参与人
- PUT    /quotations/{id}/participants/{user_id}       → 更新参与人类型
- DELETE /quotations/{id}/participants/{user_id}       → 移除参与人
- POST   /quotations/{id}/copy                         → 复制
- GET    /quotations/{id}/summary                      → 汇总
- GET    /my-assignments                               → 我的参与
- GET    /my-assigned-modules                          → 我的模块
"""

import json
from typing import Optional
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from sqlalchemy import or_, func as sa_func, text

from core.models.quotation import Quotation
from core.models.quotation import QuotationParticipant
from core.models.user import User
from core.models.module import Module, ModuleParticipant
from core.models.material import ModuleMaterial, Material
from core.models.fee import OtherFee
from core.models.fee_rate import FeeRate
from core.models.version import VersionSnapshot
from core.models.labor_hour import LaborHour
from core.models.participant_type_permission import ParticipantTypePermission
from core.models.travel import TravelPersonTripFee
from core.models.travel_entry import TravelPersonDays, TravelPersonTrip, PackingEntry
from core.models.operation_log import Action, Module as LogModule, OperationLog
from core.auth import get_db, get_current_user_id
from datetime import datetime


router = APIRouter()


# ============== 辅助函数（替代 Flask 的 MessageService 和 log_operation） ==============

def _log_op(db, user_id, action, module, resource_type=None, resource_id=None, detail=None,
            username=None):
    """记录操作日志（兼容版，使用传入的 db session）"""
    log_entry = OperationLog(
        user_id=int(user_id),
        username=username or str(user_id),
        action=action.value if hasattr(action, 'value') else action,
        module=module.value if hasattr(module, 'value') else module,
        resource_type=resource_type,
        resource_id=resource_id,
        detail=detail,
        created_at=datetime.utcnow(),
    )
    db.add(log_entry)


def _send_message(db, recipient_id, title, content, msg_type, related_id=None, related_type=None,
                  sender_id=None):
    """发送消息（raw SQL - 避免 Flask-SQLAlchemy 模型导入冲突）"""
    db.execute(
        text("""INSERT INTO messages
(sender_id, recipient_id, title, content, type, related_id, related_type, created_at, is_read)
VALUES (:sender_id, :recipient_id, :title, :content, :type, :related_id, :related_type, NOW(), false)"""),
        {
            "sender_id": sender_id,
            "recipient_id": recipient_id,
            "title": title,
            "content": content,
            "type": msg_type,
            "related_id": related_id,
            "related_type": related_type,
        }
    )


def _notify_users(db, user_ids, title, content, msg_type, related_id=None, related_type=None):
    """向多个用户发送消息"""
    from datetime import datetime
    now = datetime.utcnow()
    for uid in user_ids:
        db.execute(
            text("""INSERT INTO messages
(sender_id, recipient_id, title, content, type, related_id, related_type, created_at, is_read)
VALUES (NULL, :recipient_id, :title, :content, :type, :related_id, :related_type, :created_at, false)"""),
            {
                "recipient_id": uid,
                "title": title,
                "content": content,
                "type": msg_type,
                "related_id": related_id,
                "related_type": related_type,
                "created_at": now,
            }
        )


# ============== Pydantic 请求体 ==============

class QuotationCreate(BaseModel):
    name: str
    type: str = "single"
    scheme_no: Optional[str] = None
    business_owner_id: Optional[int] = None
    tax_rate: float = 0.13
    profit_rate: float = 0.0
    currency: str = "CNY"
    parent_id: Optional[int] = None


class QuotationUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    scheme_no: Optional[str] = None
    business_owner_id: Optional[int] = None
    tax_rate: Optional[float] = None
    profit_rate: Optional[float] = None
    currency: Optional[str] = None
    coefficients: Optional[dict] = None
    parent_id: Optional[int] = None


class StatusUpdate(BaseModel):
    status: str


class ParticipantAdd(BaseModel):
    user_id: int
    participant_type: str = "project"


class ParticipantUpdate(BaseModel):
    participant_type: str


class ArchiveRequest(BaseModel):
    remark: Optional[str] = "归档发布"


# ============== 辅助函数 ==============

def _validate_quotation(db, quotation_id):
    """验证报价单是否存在（支持数字ID或方案号）"""
    try:
        quotation = db.query(Quotation).get(int(quotation_id))
    except (ValueError, TypeError):
        quotation = None
    if not quotation:
        quotation = db.query(Quotation).filter(Quotation.scheme_no == quotation_id).first()
    if not quotation:
        raise HTTPException(status_code=404, detail="报价单不存在")
    return quotation


def _check_permission(db, user_id, permission_code):
    """检查用户是否有指定权限（管理员放行）"""
    user = db.query(User).get(int(user_id))
    if not user:
        raise HTTPException(status_code=401, detail="用户不存在")
    if user.role == 'admin':
        return True
    from core.models import Role
    role = db.query(Role).filter(Role.code == user.role).first()
    if not role:
        raise HTTPException(status_code=403, detail="没有操作权限")
    if not any(p.code == permission_code for p in role.permissions):
        raise HTTPException(status_code=403, detail="没有操作权限")
    return True


def _check_any_permission(db, user_id, *codes):
    """检查用户是否有任意一个指定权限"""
    user = db.query(User).get(int(user_id))
    if not user:
        raise HTTPException(status_code=401, detail="用户不存在")
    if user.role == 'admin':
        return True
    from core.models import Role
    role = db.query(Role).filter(Role.code == user.role).first()
    if not role:
        raise HTTPException(status_code=403, detail="没有操作权限")
    if not any(p.code in codes for p in role.permissions):
        raise HTTPException(status_code=403, detail="没有操作权限")
    return True


def _calc_person_trip_total(db, entry):
    """计算单条差旅人次费用"""
    if entry.unit_price or entry.visa_fee:
        up = float(entry.unit_price) if entry.unit_price else 0
        vf = float(entry.visa_fee) if entry.visa_fee else 0
    else:
        fee_record = db.query(TravelPersonTripFee).filter_by(
            travel_category_id=entry.travel_category_id,
            travel_mode_id=entry.travel_mode_id,
            is_active=True
        ).first()
        up = float(fee_record.unit_price or 0) if fee_record else 0
        vf = float(fee_record.visa_fee or 0) if fee_record else 0
    cat_code = entry.travel_category.code if entry.travel_category else ''
    return float(entry.person_count or 0) * (up + (vf if cat_code != 'domestic' else 0))


def _create_version_snapshot(db, quotation, operator_id, operation_type, remark=None):
    """创建版本快照（线体报价单包含所有子报价单数据）"""
    trip_fees = {
        (f.travel_category_id, f.travel_mode_id): (float(f.unit_price), float(f.visa_fee))
        for f in db.query(TravelPersonTripFee).all()
    }

    max_version = db.query(sa_func.max(VersionSnapshot.version_no)).filter_by(
        quotation_id=quotation.id
    ).scalar() or 0

    if quotation.type == 'line':
        child_ids = [c.id for c in quotation.children.all()]
        all_ids = [quotation.id] + child_ids
    else:
        all_ids = [quotation.id]

    all_modules = db.query(Module).filter(Module.quotation_id.in_(all_ids)).all()
    all_fees = db.query(OtherFee).filter(OtherFee.quotation_id.in_(all_ids)).all()
    all_labor = db.query(LaborHour).filter(LaborHour.quotation_id.in_(all_ids)).all()

    snapshot_data = {
        'name': quotation.name,
        'type': quotation.type,
        'scheme_no': quotation.scheme_no,
        'tax_rate': float(quotation.tax_rate) if quotation.tax_rate else 0,
        'profit_rate': float(quotation.profit_rate) if quotation.profit_rate else 0,
        'business_owner_id': quotation.business_owner_id,
        'coefficients': quotation.coefficients or {'large': 1.0, 'standard': 1.0, 'other': 1.0},
        'modules': [{
            'id': m.id,
            'quotation_id': m.quotation_id,
            'name': m.name,
            'code': m.code,
            'materials': [{
                'id': mm.id,
                'material_id': mm.material_id,
                'name': mm.material.name if mm.material else None,
                'brand': mm.material.brand if mm.material else None,
                'spec': mm.material.spec if mm.material else None,
                'unit_price': float(mm.material.unit_price) if mm.material and mm.material.unit_price else 0,
                'quantity': float(mm.quantity),
                'selected_by_id': mm.selected_by_id,
                'category': mm.material.category if mm.material else 'standard',
                'is_other': mm.is_other,
                'unit_price_override': float(mm.unit_price_override) if mm.unit_price_override else None
            } for mm in db.query(ModuleMaterial).filter_by(module_id=m.id).all()]
        } for m in all_modules],
        'fees': [{
            'quotation_id': f.quotation_id,
            'fee_type': f.fee_type,
            'location': f.location,
            'amount': float(f.amount) if f.amount else 0,
            'description': f.description
        } for f in all_fees],
        'labor_hours': [{
            'quotation_id': l.quotation_id,
            'name': l.name,
            'hours': float(l.hours) if l.hours else 0,
            'unit_price': float(l.unit_price) if l.unit_price else 0,
            'total': float(l.total) if l.total else 0
        } for l in all_labor],
        'packing_entries': [{
            'id': pe.id,
            'packing_type_name': pe.packing_type.name if pe.packing_type else None,
            'quantity': float(pe.quantity) if pe.quantity else 0,
            'unit_price': float(pe.unit_price) if pe.unit_price else (
                float(pe.packing_type.unit_price) if pe.packing_type and pe.packing_type.unit_price else 0),
            'total': float(
                (float(pe.unit_price) if pe.unit_price else (
                    float(pe.packing_type.unit_price) if pe.packing_type and pe.packing_type.unit_price else 0))
                * float(pe.quantity or 0)),
        } for pe in db.query(PackingEntry).filter(PackingEntry.quotation_id.in_(all_ids)).all()],
        'person_days_entries': [{
            'id': pd.id,
            'destination': pd.travel_category.name if pd.travel_category else None,
            'days': float(pd.person_days) if pd.person_days else 0,
            'quantity': float(pd.person_days) if pd.person_days else 0,
            'unit_price': float(pd.unit_price) if pd.unit_price else (
                float(pd.travel_category.day_rates[0].unit_price)
                if pd.travel_category and pd.travel_category.day_rates else 0),
            'total': float(
                (float(pd.unit_price) if pd.unit_price else (
                    float(pd.travel_category.day_rates[0].unit_price)
                    if pd.travel_category and pd.travel_category.day_rates else 0))
                * float(pd.person_days or 0)),
        } for pd in db.query(TravelPersonDays).filter(TravelPersonDays.quotation_id.in_(all_ids)).all()],
        'person_trip_entries': [{
            'id': pt.id,
            'destination': f"{pt.travel_category.name if pt.travel_category else ''} {pt.travel_mode.name if pt.travel_mode else ''}".strip(),
            'quantity': float(pt.person_count) if pt.person_count else 0,
            'unit_price': float(pt.unit_price) if pt.unit_price else (
                trip_fees.get((pt.travel_category_id, pt.travel_mode_id), (0, 0))[0]),
            'visa_fee': float(pt.visa_fee) if pt.visa_fee else (
                trip_fees.get((pt.travel_category_id, pt.travel_mode_id), (0, 0))[1]),
            'total': float(
                ((float(pt.unit_price) if pt.unit_price else (
                    trip_fees.get((pt.travel_category_id, pt.travel_mode_id), (0, 0))[0]))
                 + (float(pt.visa_fee) if pt.visa_fee else (
                    trip_fees.get((pt.travel_category_id, pt.travel_mode_id), (0, 0))[1])))
                * float(pt.person_count or 0)),
        } for pt in db.query(TravelPersonTrip).filter(TravelPersonTrip.quotation_id.in_(all_ids)).all()],
    }

    new_version_no = max_version + 1

    version = VersionSnapshot(
        quotation_id=quotation.id,
        version_no=new_version_no,
        snapshot_data=json.dumps(snapshot_data, ensure_ascii=False),
        operation_type=operation_type,
        remark=remark,
        operator_id=operator_id
    )
    db.add(version)
    db.flush()

    # 归档/重做的 PDF 生成统一由 archive_quotation 路由里的同步 generate_version_pdfs 完成（与 Tab 格式一致）
    # 这里不再启动异步线程，避免 generate_version_files 用 _generate_version_pdf（明细+汇总格式）覆盖 pdf_file 字段
    # 异步生成版本文件（已禁用：与 archive_quotation 同步逻辑重复）
    async_quotation_id = quotation.id
    async_snapshot_data = json.dumps(snapshot_data, ensure_ascii=False)
    async_version_no = new_version_no

    return version


# ============== 端点实现 ==============

@router.get("/quotations")
def get_quotations(
    db=Depends(get_db),
    user_id: str = Depends(get_current_user_id),
    status: Optional[str] = Query(None),
    type: Optional[str] = Query(None, alias="type"),
    parent_only: Optional[str] = Query(None),
    parent_id: Optional[int] = Query(None),
    keyword: Optional[str] = Query(None),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=200, description="每页条数"),
):
    user = db.query(User).get(int(user_id))

    # 同时查父报价单和子报价单（父报价单分页，子报价单作为 _children 内联）
    # 先查所有匹配的报价单
    query = db.query(Quotation)

    # 普通用户只能看到自己参与的报价单
    if user.role != 'admin':
        query = query.outerjoin(QuotationParticipant).filter(
            or_(
                QuotationParticipant.user_id == user_id,
                Quotation.business_owner_id == user_id
            )
        )

    if status:
        query = query.filter(Quotation.status == status)
    if type:
        query = query.filter(Quotation.type == type)
    if parent_only == 'true':
        query = query.filter(Quotation.parent_id.is_(None))
    if parent_id is not None:
        query = query.filter(Quotation.parent_id == parent_id)
    if keyword:
        query = query.filter(
            or_(
                Quotation.name.like(f'%{keyword}%'),
                Quotation.scheme_no.like(f'%{keyword}%')
            )
        )

    # 一次性取所有数据（含 child_count，不分页）
    # ⚠️ 不能用 .distinct() 因为 outerjoin 会造成重复行
    all_quotations = query.order_by(Quotation.created_at.desc()).all()

    # 分离父子（去重：outerjoin 可能导致重复）
    seen_ids = set()
    parents = []
    children_map = {}
    for q in all_quotations:
        if q.id in seen_ids:
            continue
        seen_ids.add(q.id)
        qd = q.to_dict()
        if q.parent_id:
            # 子报价单
            if q.parent_id not in children_map:
                children_map[q.parent_id] = []
            children_map[q.parent_id].append(qd)
        else:
            parents.append(qd)

    # 计算总父报价单数
    total_parents = len(parents)

    # 分页（只在父报价单上分页）
    start = (page - 1) * page_size
    end = start + page_size
    page_parents = parents[start:end]

    # 给当前页的父报价单附加子报价单
    for qd in page_parents:
        cids = children_map.pop(qd['id'], [])
        if cids:
            qd['_children'] = cids
            qd['child_count'] = len(cids)
        else:
            qd['child_count'] = 0

    return JSONResponse(content={
        "items": page_parents,
        "total": total_parents,
        "page": page,
        "page_size": page_size,
    }, status_code=200)


@router.post("/quotations")
def create_quotation(
    body: QuotationCreate,
    db=Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    _check_permission(db, int(user_id), 'quotation.create')
    user = db.query(User).get(int(user_id))

    # 校验：非子报价单（parent_id 为空）的 scheme_no 全局唯一
    if body.scheme_no and body.parent_id is None:
        existing = db.query(Quotation).filter(
            Quotation.scheme_no == body.scheme_no,
            Quotation.parent_id.is_(None),
        ).first()
        if existing:
            raise HTTPException(
                status_code=400,
                detail=f'方案号 "{body.scheme_no}" 已被非子报价单 "{existing.name}" 使用，不能重复使用'
            )

    quotation = Quotation(
        name=body.name,
        type=body.type,
        scheme_no=body.scheme_no,
        status='draft',
        creator_id=int(user_id),
        business_owner_id=body.business_owner_id,
        tax_rate=body.tax_rate,
        profit_rate=body.profit_rate,
        currency=body.currency,
        parent_id=body.parent_id
    )
    db.add(quotation)
    db.commit()

    _log_op(db, user_id,
        action=Action.CREATE,
        module=LogModule.QUOTATION,
        resource_type='quotation',
        resource_id=quotation.scheme_no or str(quotation.id),
        detail=f'创建报价单 "{quotation.name}"'
    )

    return JSONResponse(content=quotation.to_dict(), status_code=201)

# ---- 方案号查询（代理外部接口）----

@router.get("/quotations/scheme-search")
def search_scheme_no(
    prefix: str = Query("", description="方案号前缀，例如 CS00"),
    db=Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    """方案号联动查询 - 代理外部方案库接口。

    前端在「新增报价单」页面的「方案号」输入框失焦时调用，传入用户已输入的前缀，
    返回外部方案库中匹配的所有方案号 + 状态信息，用于：
    1. 自动补全 / 推荐可用方案号
    2. 避免用户输入已被占用的方案号

    外部接口：POST http://222.92.47.101/prod-api/scheme/list
    """
    import requests as _req

    _check_permission(db, int(user_id), 'quotation.create')

    # 调外部接口
    external_url = "http://222.92.47.101/prod-api/scheme/list"
    payload = {
        "generate": "or",
        "conditionList": [
            {"fieldName": "schemeNo", "fieldValue": prefix, "operation": "LIKE"},
            {"fieldName": "schemeName", "fieldValue": prefix, "operation": "LIKE"},
        ],
        "order": {"field": "createTime", "order": "desc"},
    }
    try:
        resp = _req.post(external_url, json=payload, timeout=8)
        resp.raise_for_status()
        body = resp.json()
    except _req.RequestException as e:
        raise HTTPException(status_code=502, detail=f"方案库接口调用失败: {e}")
    except ValueError as e:
        raise HTTPException(status_code=502, detail=f"方案库响应不是 JSON: {e}")

    if body.get("code") != 0:
        raise HTTPException(status_code=502, detail=f"方案库返回错误: {body}")

    # 提取关键字段 + 标注是否已被本地报价单使用
    rows = body.get("data") or []
    used_scheme_nos = set(
        row[0] for row in db.query(Quotation.scheme_no)
        .filter(Quotation.scheme_no.isnot(None), Quotation.parent_id.is_(None))
        .all()
    )
    # 透传外部接口的字段（业务负责人/项目负责人等用于自动填表）
    # + 标注 is_used_locally 供前端判断是否已被本系统使用
    FORWARDED_FIELDS = [
        "schemeId", "schemeNo", "schemeName", "schemeSpec", "craftType",
        "customerName", "schemeLocation", "schemeHours",
        "schemeStatus", "archiveStatus", "contractCode",
        "operatorNo", "operatorName",
        "businessManager", "businessManagerName", "businessManagerPhone",
        "projectOrganization", "projectOrganizationName", "projectOrganizationPhone",
        "projectManager", "projectManagerName", "projectManagerPhone",
        "createTime", "updateTime",
    ]
    result = []
    for item in rows:
        sn = item.get("schemeNo")
        if not sn:
            continue
        out = {f: item.get(f) for f in FORWARDED_FIELDS}
        out["is_used_locally"] = sn in used_scheme_nos
        result.append(out)
    return JSONResponse(content={
        "total": len(result),
        "items": result,
    }, status_code=200)


# ---- 趋势统计（按月聚合 + 散点）----

@router.get("/quotations/trends")
def get_quotation_trends(
    db=Depends(get_db),
    user_id: str = Depends(get_current_user_id),
    months: int = Query(6, ge=1, le=24, description="最近 N 个月"),
):
    """报价单趋势统计：按月聚合数量、利润率、工时 + 利润率散点

    返回结构（前端 ECharts 友好）：
    {
        "summary": {
            "total_count": 26,
            "total_approved": 11,
            "avg_gross_margin": 0.157,     # 实际毛利率（profit_rate/(1+profit_rate)）
            "avg_profit_rate": 0.186,      # 对外利润率（利润/成本，审计用）
            "current_month_count": 3
        },
        "monthly": [
            {"period": "2026-01", "count": 5, "approved": 3, "draft": 1,
             "avg_gross_margin": 0.157, "avg_profit_rate": 0.18,
             "total_hours": 120.0},
            ...
        ],
        "by_status": [
            {"status": "approved", "count": 11},
            ...
        ],
        "by_type": [
            {"type": "single", "count": 13},
            ...
        ],
        "scatter": [
            {"id": 1, "name": "...", "profit_rate": 0.15, "gross_margin": 0.130,
             "total_hours": 80, "month": "2026-01"},
            ...
        ],
        "insights": ["毛利率上升 5 个百分点", ...]
    }

    字段约定（与 ai_tools.py 保持一致）：
    - profit_rate = 利润/成本（对外利润率，行业惯用）
    - gross_margin = profit_rate/(1+profit_rate)（实际毛利率 = 利润/售价，用户视角）
    用户问"利润率"时，业务视角是 gross_margin 不是 profit_rate。
    """
    from datetime import datetime
    from dateutil.relativedelta import relativedelta
    from sqlalchemy import func, case

    # 起算时间：当前月往前 N 个月
    now = datetime.now()
    start = (now - relativedelta(months=months - 1)).replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    # 1) 月度聚合
    # 关键：profit_rate = 利润/成本（对外利润率），gross_margin = profit_rate/(1+profit_rate)（实际毛利率）
    # 用户业务视角是 gross_margin，所以先在 SQL 里算好
    monthly_rows = db.query(
        func.to_char(Quotation.created_at, 'YYYY-MM').label('period'),
        func.count(Quotation.id).label('count'),
        func.sum(case((Quotation.status == 'approved', 1), else_=0)).label('approved'),
        func.sum(case((Quotation.status == 'draft', 1), else_=0)).label('draft'),
        func.avg(Quotation.profit_rate).label('avg_profit'),
        func.avg(Quotation.profit_rate / (1 + Quotation.profit_rate)).label('avg_gross'),
    ).filter(
        Quotation.created_at >= start
    ).group_by('period').order_by('period').all()

    monthly = []
    for r in monthly_rows:
        monthly.append({
            "period": r.period,
            "count": int(r.count or 0),
            "approved": int(r.approved or 0),
            "draft": int(r.draft or 0),
            "avg_profit_rate": round(float(r.avg_profit or 0), 4),
            "avg_gross_margin": round(float(r.avg_gross or 0), 4),
            "total_hours": 0.0,  # labor_hours 表当前为空，后续可补
        })

    # 2) 状态分布
    status_rows = db.query(
        Quotation.status, func.count(Quotation.id)
    ).filter(Quotation.created_at >= start).group_by(Quotation.status).all()
    by_status = [{"status": s, "count": int(c)} for s, c in status_rows]

    # 3) 类型分布
    type_rows = db.query(
        Quotation.type, func.count(Quotation.id)
    ).filter(Quotation.created_at >= start).group_by(Quotation.type).all()
    by_type = [{"type": t, "count": int(c)} for t, c in type_rows]

    # 4) 利润率散点（每个报价单一个点）
    scatter_rows = db.query(
        Quotation.id, Quotation.name, Quotation.profit_rate,
        Quotation.status, Quotation.created_at
    ).filter(
        Quotation.created_at >= start,
        Quotation.profit_rate.isnot(None),
    ).all()
    scatter = [
        {
            "id": r.id,
            "name": r.name,
            "profit_rate": round(float(r.profit_rate), 4),
            "gross_margin": round(float(r.profit_rate) / (1 + float(r.profit_rate)), 4),
            "status": r.status,
            "month": r.created_at.strftime('%Y-%m'),
        }
        for r in scatter_rows
    ]

    # 5) 顶部统计
    total_count = sum(m['count'] for m in monthly)
    total_approved = sum(m['approved'] for m in monthly)
    current_month = now.strftime('%Y-%m')
    current_month_count = next((m['count'] for m in monthly if m['period'] == current_month), 0)

    # 平均利润率（对外）+ 平均毛利率（实际）
    # 两种算法：①纯字段平均（已对外），②先算毛利率再平均（更精确）
    # 这里采用"算毛利率再平均"，与 ai_tools.py 的 get_quotation_gross_margin 保持一致
    raw_profits = db.query(Quotation.profit_rate).filter(
        Quotation.created_at >= start,
        Quotation.profit_rate.isnot(None),
        Quotation.profit_rate > 0,  # 避免除 0
    ).all()
    profit_list = [float(r[0]) for r in raw_profits]
    avg_profit_overall = sum(profit_list) / len(profit_list) if profit_list else 0
    avg_gross_overall = sum(p / (1 + p) for p in profit_list) / len(profit_list) if profit_list else 0

    # 6) 洞察（同比/环比）—— 业务视角用毛利率 gross_margin
    insights = []
    if len(monthly) >= 2:
        latest = monthly[-1]['avg_gross_margin']
        earliest = monthly[0]['avg_gross_margin']
        diff_pp = round((latest - earliest) * 100, 1)
        if diff_pp > 1:
            insights.append(f"📈 最近月比首月毛利率提升 {diff_pp} 个百分点")
        elif diff_pp < -1:
            insights.append(f"📉 最近月比首月毛利率下降 {abs(diff_pp)} 个百分点，需关注")
        else:
            insights.append(f"➡️ 毛利率保持稳定（波动 {abs(diff_pp)} 个百分点）")

        latest_count = monthly[-1]['count']
        earliest_count = monthly[0]['count']
        if latest_count > earliest_count:
            insights.append(f"📊 报价单数量增长 {latest_count - earliest_count} 单")
        elif latest_count < earliest_count:
            insights.append(f"📉 报价单数量减少 {earliest_count - latest_count} 单")

    # 毛利率健康度（用已通过的实际毛利率）
    approved_gross = [s['gross_margin'] for s in scatter if s['status'] == 'approved']
    if approved_gross:
        avg_approved_gross = sum(approved_gross) / len(approved_gross)
        if avg_approved_gross < 0.10:
            insights.append(f"⚠️ 已通过报价单平均毛利率仅 {avg_approved_gross*100:.1f}%，建议检查成本结构")
        elif avg_approved_gross > 0.20:
            insights.append(f"✨ 已通过报价单平均毛利率 {avg_approved_gross*100:.1f}%，高于行业水平")

    return {
        "summary": {
            "total_count": total_count,
            "total_approved": total_approved,
            "avg_gross_margin": round(float(avg_gross_overall), 4),  # 实际毛利率（业务视角）
            "avg_profit_rate": round(float(avg_profit_overall), 4),  # 对外利润率（审计视角）
            "current_month_count": current_month_count,
        },
        "monthly": monthly,
        "by_status": by_status,
        "by_type": by_type,
        "scatter": scatter,
        "insights": insights,
        "params": {"months": months, "start_period": start.strftime('%Y-%m')},
    }


# ---- 我的参与 ----

@router.get("/quotations/my-assignments")
def get_my_assignments(
    db=Depends(get_db),
    user_id: str = Depends(get_current_user_id),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=200, description="每页条数"),
):
    uid = int(user_id)
    user = db.query(User).get(uid)
    if not user:
        raise HTTPException(status_code=401, detail='用户不存在')

    # 分页查参与记录
    base_query = db.query(QuotationParticipant).filter_by(user_id=uid)
    total = base_query.count()
    participant_records = base_query.order_by(QuotationParticipant.created_at.desc())\
        .offset((page - 1) * page_size).limit(page_size).all()

    if not participant_records:
        return JSONResponse(content={"items": [], "total": 0, "page": page, "page_size": page_size}, status_code=200)

    # 批量查报价单
    qids = [p.quotation_id for p in participant_records]
    quotations = db.query(Quotation).filter(Quotation.id.in_(qids)).all()
    q_map = {q.id: q for q in quotations}

    # 批量查模块数和物料数
    module_counts = dict(
        db.query(Module.quotation_id, sa_func.count(Module.id))
        .filter(Module.quotation_id.in_(qids))
        .group_by(Module.quotation_id).all()
    )
    material_counts = dict(
        db.query(Module.quotation_id, sa_func.count(ModuleMaterial.id))
        .join(Module, ModuleMaterial.module_id == Module.id)
        .filter(Module.quotation_id.in_(qids))
        .group_by(Module.quotation_id).all()
    )

    result = []
    for p in participant_records:
        quotation = q_map.get(p.quotation_id)
        if not quotation:
            continue
        result.append({
            'quotation_id': quotation.id,
            'quotation_name': quotation.name,
            'quotation_scheme_no': quotation.scheme_no,
            'quotation_status': quotation.status,
            'participant_type': p.participant_type,
            'business_owner_name': quotation.business_owner.real_name if quotation.business_owner else None,
            'module_count': module_counts.get(p.quotation_id, 0),
            'material_count': material_counts.get(p.quotation_id, 0),
            'created_at': quotation.created_at.isoformat() if quotation.created_at else None,
        })

    return JSONResponse(content={
        "items": result,
        "total": total,
        "page": page,
        "page_size": page_size,
    }, status_code=200)


@router.get("/quotations/my-assigned-modules")
def get_my_assigned_modules(
    db=Depends(get_db),
    user_id: str = Depends(get_current_user_id),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=200, description="每页条数"),
):
    uid = int(user_id)
    user = db.query(User).get(uid)
    if not user:
        raise HTTPException(status_code=401, detail='用户不存在')

    # 分页查模块参与记录
    base_query = db.query(ModuleParticipant).filter_by(user_id=uid)
    total = base_query.count()
    participant_records = base_query.order_by(ModuleParticipant.created_at.desc())\
        .offset((page - 1) * page_size).limit(page_size).all()

    if not participant_records:
        return JSONResponse(content={"items": [], "total": 0, "page": page, "page_size": page_size}, status_code=200)

    module_ids = [p.module_id for p in participant_records]
    modules = db.query(Module).filter(Module.id.in_(module_ids)).all()
    mod_map = {m.id: m for m in modules}

    # 批量查物料数
    material_counts = dict(
        db.query(ModuleMaterial.module_id, sa_func.count(ModuleMaterial.id))
        .filter(ModuleMaterial.module_id.in_(module_ids))
        .group_by(ModuleMaterial.module_id).all()
    )

    # 批量查报价单
    qids = list(set(m.quotation_id for m in modules if m.quotation_id))
    q_map = {}
    if qids:
        quotations = db.query(Quotation).filter(Quotation.id.in_(qids)).all()
        q_map = {q.id: q for q in quotations}

    result = []
    for mod in modules:
        quotation = q_map.get(mod.quotation_id)
        result.append({
            'id': mod.id,
            'module_name': mod.name,
            'module_code': mod.code,
            'quotation_id': mod.quotation_id,
            'quotation_name': quotation.name if quotation else None,
            'quotation_scheme_no': quotation.scheme_no if quotation else None,
            'quotation_status': quotation.status if quotation else None,
            'material_count': material_counts.get(mod.id, 0),
        })

    return JSONResponse(content={
        "items": result,
        "total": total,
        "page": page,
        "page_size": page_size,
    }, status_code=200)


@router.get("/quotations/{quotation_id}")
def get_quotation(
    quotation_id: int,
    db=Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    quotation = _validate_quotation(db, quotation_id)
    return JSONResponse(content=quotation.to_dict(), status_code=200)


@router.get("/quotations/{quotation_id}/permissions")
def get_quotation_permissions(
    quotation_id: int,
    db=Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    quotation = _validate_quotation(db, quotation_id)
    uid = int(user_id)

    participant = db.query(QuotationParticipant).filter_by(
        quotation_id=quotation.id,
        user_id=uid
    ).first()

    if quotation.business_owner_id == uid:
        all_tabs = [p.tab_name for p in db.query(ParticipantTypePermission).filter_by(
            participant_type='project', is_disabled=False).all()]
        return {
            'participant_type': 'owner',
            'can_edit_coefficients': True,
            'can_edit_participants': True,
            'can_edit_materials': True,
            'can_edit_modules': True,
            'can_edit_fees': True,
            'tabs': all_tabs
        }

    if not participant:
        return {
            'participant_type': None,
            'can_edit_coefficients': False,
            'can_edit_participants': False,
            'can_edit_materials': False,
            'can_edit_modules': False,
            'can_edit_fees': False,
            'tabs': ['summary']
        }

    ptype = participant.participant_type
    perms = db.query(ParticipantTypePermission).filter_by(
        participant_type=ptype, is_disabled=False).order_by(
        ParticipantTypePermission.sort_order).all()
    tabs = [p.tab_name for p in perms]

    can_edit_materials = 'materials' in tabs
    can_edit_modules = 'modules' in tabs
    can_edit_fees = 'fees' in tabs
    can_edit_participants = 'participants' in tabs
    can_edit_coefficients = 'coefficients' in tabs

    return {
        'participant_type': ptype,
        'can_edit_coefficients': can_edit_coefficients,
        'can_edit_participants': can_edit_participants,
        'can_edit_materials': can_edit_materials,
        'can_edit_modules': can_edit_modules,
        'can_edit_fees': can_edit_fees,
        'tabs': tabs
    }


@router.put("/quotations/{quotation_id}")
def update_quotation(
    quotation_id: int,
    body: QuotationUpdate,
    db=Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    _check_permission(db, int(user_id), 'quotation.edit')
    quotation = _validate_quotation(db, quotation_id)

    data = body.model_dump(exclude_unset=True)
    # 校验：非子报价单的 scheme_no 不能改成已存在的值
    if 'scheme_no' in data and data['scheme_no'] and (data.get('parent_id', quotation.parent_id) is None):
        new_sn = data['scheme_no']
        if new_sn != quotation.scheme_no:  # 真的在改
            existing = db.query(Quotation).filter(
                Quotation.scheme_no == new_sn,
                Quotation.parent_id.is_(None),
                Quotation.id != quotation_id,  # 排除自己
            ).first()
            if existing:
                raise HTTPException(
                    status_code=400,
                    detail=f'方案号 "{new_sn}" 已被非子报价单 "{existing.name}" 使用，不能重复使用'
                )
    if 'name' in data:
        quotation.name = data['name']
    if 'type' in data:
        quotation.type = data['type']
    if 'scheme_no' in data:
        quotation.scheme_no = data['scheme_no']
    if 'business_owner_id' in data:
        quotation.business_owner_id = data['business_owner_id']
    if 'tax_rate' in data:
        quotation.tax_rate = data['tax_rate']
    if 'profit_rate' in data:
        quotation.profit_rate = data['profit_rate']
    if 'currency' in data:
        quotation.currency = data['currency']
    if 'coefficients' in data:
        quotation.coefficients = data['coefficients']
    if 'parent_id' in data:
        quotation.parent_id = data['parent_id']

    db.commit()
    return JSONResponse(content=quotation.to_dict(), status_code=200)


@router.delete("/quotations/{quotation_id}")
def delete_quotation(
    quotation_id: int,
    db=Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    _check_permission(db, int(user_id), 'quotation.delete')
    quotation = _validate_quotation(db, quotation_id)

    if quotation.type == 'line' and quotation.children.count() > 0:
        raise HTTPException(
            status_code=400,
            detail='该线体报价单下存在子报价单，请先删除子报价单'
        )

    detail = f'删除报价单 "{quotation.name}" ({quotation.scheme_no or quotation.id})'
    db.delete(quotation)
    db.commit()

    _log_op(db, user_id,
        action=Action.DELETE,
        module=LogModule.QUOTATION,
        resource_type='quotation',
        resource_id=str(quotation.id),
        detail=detail
    )
    return JSONResponse(content={'message': '删除成功'}, status_code=200)


@router.put("/quotations/{quotation_id}/status")
def update_status(
    quotation_id: int,
    body: StatusUpdate,
    db=Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    _check_permission(db, int(user_id), 'quotation.edit')

    quotation = db.query(Quotation).get(quotation_id)
    if not quotation:
        raise HTTPException(status_code=404, detail='报价单不存在')

    new_status = body.status

    valid_transitions = {
        'draft': ['approved'],
        'approved': ['draft'],
    }

    if new_status not in ['draft', 'approved']:
        raise HTTPException(status_code=400, detail='无效的状态')

    if quotation.parent_id:
        if new_status == 'approved':
            raise HTTPException(
                status_code=400,
                detail='该报价单属于线体报价单，请通过线体报价单归档'
            )
        if new_status == 'draft':
            raise HTTPException(
                status_code=400,
                detail='该报价单属于线体报价单，请通过线体报价单撤销归档'
            )

    if new_status != quotation.status:
        if new_status not in valid_transitions.get(quotation.status, []):
            raise HTTPException(
                status_code=400,
                detail=f'不能从 {quotation.status} 转换到 {new_status}'
            )

        old_status = quotation.status
        quotation.status = new_status

        # 线体归档时同步归档所有子报价单
        if quotation.type == 'line' and new_status == 'approved':
            for child in quotation.children.all():
                if child.status == 'draft':
                    child.status = 'approved'
                    child_version = _create_version_snapshot(
                        db, child, int(user_id), 'archive', '随线体报价单归档')
                    # 异步 PDF 生成在 _create_version_snapshot 内处理

        # 线体撤销归档时同步撤销所有子报价单
        if quotation.type == 'line' and new_status == 'draft':
            for child in quotation.children.all():
                if child.status == 'approved':
                    child.status = 'draft'

        db.commit()

        if new_status == 'approved':
            version = _create_version_snapshot(
                db, quotation, int(user_id), 'archive', '归档发布')
            _log_op(db, int(user_id),
                action=Action.EDIT,
                module=LogModule.QUOTATION,
                resource_type='quotation',
                resource_id=str(quotation.id),
                detail=f'归档报价单 "{quotation.name}"'
            )
        else:
            _log_op(db, int(user_id),
                action=Action.EDIT,
                module=LogModule.QUOTATION,
                resource_type='quotation',
                resource_id=str(quotation.id),
                detail=f'撤销归档 "{quotation.name}"'
            )

    return JSONResponse(content=quotation.to_dict(), status_code=200)


# ---- 版本相关 ----

@router.get("/quotations/{quotation_id}/versions")
def get_versions(
    quotation_id: int,
    db=Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    quotation = db.query(Quotation).get(quotation_id)
    if not quotation:
        raise HTTPException(status_code=404, detail='报价单不存在')

    versions = db.query(VersionSnapshot).filter_by(
        quotation_id=quotation_id
    ).order_by(VersionSnapshot.version_no.desc()).all()

    return JSONResponse(content=[v.to_dict() for v in versions], status_code=200)



# ──────────────────────────────────────────────
# 版本对比（必须在 /versions/{version_no} 之前注册，否则会被它拦截把 "compare" 当 version_no 报 422）
# ──────────────────────────────────────────────

@router.get('/quotations/{quotation_id}/versions/compare')
def compare_versions_by_quotation(
    quotation_id: int,
    v1: int = Query(..., description='版本号 v1'),
    v2: int = Query(..., description='版本号 v2'),
    db=Depends(get_db),
):
    """对比同一报价单的两个版本（按 version_no）"""
    v1_obj = (
        db.query(VersionSnapshot)
        .filter_by(quotation_id=quotation_id, version_no=v1)
        .first()
    )
    v2_obj = (
        db.query(VersionSnapshot)
        .filter_by(quotation_id=quotation_id, version_no=v2)
        .first()
    )
    if not v1_obj or not v2_obj:
        raise HTTPException(status_code=404, detail='版本不存在')

    # 线体报价单：聚合所有子报价单同 version_no 的快照数据
    quotation = db.query(Quotation).get(quotation_id)
    if quotation and quotation.type == 'line':
        child_ids = [c.id for c in quotation.children]
        extra_snapshots_v1 = (
            db.query(VersionSnapshot)
            .filter(
                VersionSnapshot.quotation_id.in_(child_ids),
                VersionSnapshot.version_no == v1,
            )
            .all()
        )
        extra_snapshots_v2 = (
            db.query(VersionSnapshot)
            .filter(
                VersionSnapshot.quotation_id.in_(child_ids),
                VersionSnapshot.version_no == v2,
            )
            .all()
        )
    else:
        extra_snapshots_v1 = []
        extra_snapshots_v2 = []

    # 复用已有的 compare logic，复用 normalize/enrich
    def normalize(snapshot):
        if 'quotation' in snapshot:
            return snapshot
        if 'modules' in snapshot or 'fees' in snapshot:
            coeff = snapshot.get('coefficients')
            return {
                'quotation': snapshot,
                'modules': snapshot.get('modules', []),
                'fees': snapshot.get('fees', []),
                'labor_hours': snapshot.get('labor_hours', []),
                'packing_entries': snapshot.get('packing_entries', []),
                'person_days_entries': snapshot.get('person_days_entries', []),
                'person_trip_entries': snapshot.get('person_trip_entries', []),
                'coefficients': coeff,
            }
        coeff = snapshot.get('coefficients')
        return {
            'quotation': snapshot,
            'modules': [],
            'fees': [],
            'labor_hours': snapshot.get('labor_hours', []),
            'packing_entries': snapshot.get('packing_entries', []),
            'person_days_entries': snapshot.get('person_days_entries', []),
            'person_trip_entries': snapshot.get('person_trip_entries', []),
            'coefficients': coeff,
        }

    material_cache = {}

    def enrich_material(mat_data):
        if not mat_data:
            return mat_data
        mat_id = mat_data.get('material_id')
        if not mat_id:
            return mat_data
        if mat_id not in material_cache:
            mat = db.query(Material).get(mat_id)
            if mat:
                material_cache[mat_id] = {
                    'material_name': mat.name,
                    'spec': mat.spec,
                    'brand': mat.brand,
                    'unit_price': float(mat.unit_price) if mat.unit_price else 0,
                    'unit': mat.unit,
                }
            else:
                material_cache[mat_id] = {
                    'material_name': f'物料{mat_id}',
                    'spec': '-',
                    'brand': '-',
                    'unit_price': 0,
                    'unit': '',
                }
        return {**mat_data, **material_cache[mat_id]}

    def enrich_module(mod):
        if 'materials' in mod:
            mod['materials'] = [enrich_material(m) for m in mod['materials']]
        return mod

    v1_data = normalize(json.loads(v1_obj.snapshot_data))
    v2_data = normalize(json.loads(v2_obj.snapshot_data))

    # 线体主报价单的 snapshot 在归档时已聚合子报价单数据
    # （_create_version_snapshot 用 all_ids=[主]+子 一次聚合）
    # 所以这里不需要再 merge，否则 labor_hours/modules 等会重复。
    # extra_snapshots_v1/v2 留作接口兼容返回，但不再合并。
    _ = extra_snapshots_v1, extra_snapshots_v2

    v1_data['modules'] = [enrich_module(m) for m in v1_data.get('modules', [])]
    v2_data['modules'] = [enrich_module(m) for m in v2_data.get('modules', [])]

    from core.services.export_service import calculate_version_totals
    v1_totals = calculate_version_totals(v1_data)
    v2_totals = calculate_version_totals(v2_data)

    return JSONResponse(content={
        'quotation_id': quotation_id,
        'version1': v1_data,
        'version_no1': v1_obj.version_no,
        'version2': v2_data,
        'version_no2': v2_obj.version_no,
        'totals1': v1_totals,
        'totals2': v2_totals,
        'created_at1': v1_obj.created_at.isoformat() if v1_obj.created_at else None,
        'created_at2': v2_obj.created_at.isoformat() if v2_obj.created_at else None,
        'operator_name1': v1_obj.operator.username if v1_obj.operator else None,
        'operator_name2': v2_obj.operator.username if v2_obj.operator else None,
    })


@router.get("/quotations/{quotation_id}/versions/{version_no}")
def get_version_detail(
    quotation_id: int,
    version_no: int,
    db=Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    version = db.query(VersionSnapshot).filter_by(
        quotation_id=quotation_id,
        version_no=version_no
    ).first()

    if not version:
        raise HTTPException(status_code=404, detail='版本不存在')

    return {
        **version.to_dict(),
        'snapshot_data': json.loads(version.snapshot_data)
    }


# ---- 归档/撤销归档 ----

@router.post("/quotations/{quotation_id}/archive")
def archive_quotation(
    quotation_id: int,
    body: ArchiveRequest = ArchiveRequest(),
    db=Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    _check_permission(db, int(user_id), 'quotation.edit')
    quotation = db.query(Quotation).get(quotation_id)
    if not quotation:
        raise HTTPException(status_code=404, detail='报价单不存在')

    if quotation.status == 'approved':
        raise HTTPException(status_code=400, detail='报价单已经归档')

    remark = body.remark
    version = _create_version_snapshot(db, quotation, int(user_id), 'archive', remark)
    db.commit()  # 必须先 commit，让 VersionSnapshot 在 DB 可见，generate_version_pdfs 才能查到

    # 归档时生成中英 PDF（无 Flask - 直接调导出服务）
    try:
        print(f"[archive {quotation_id}] generate_version_pdfs start", flush=True)
        from core.services.export_service import generate_version_pdfs
        # 纯 SQLAlchemy session，不需要 Flask app context
        result = generate_version_pdfs(quotation.id, version.version_no)
        print(f"[archive {quotation_id}] generate_version_pdfs result: {result}", flush=True)
    except Exception as e:
        import traceback
        print(f"生成版本 PDF 失败: {e}", flush=True)
        traceback.print_exc()

    quotation.status = 'approved'

    if quotation.type == 'line':
        for child in quotation.children.all():
            if child.status == 'draft':
                child.status = 'approved'
                child_version = _create_version_snapshot(
                    db, child, int(user_id), 'archive', '随线体报价单归档')
                db.commit()  # 同样：子版本需先 commit
                try:
                    from core.services.export_service import generate_version_pdfs
                    # 纯 SQLAlchemy session，不需要 Flask app context
                    generate_version_pdfs(child.id, child_version.version_no)
                except Exception as e:
                    import traceback
                    print(f"生成子报价单版本 PDF 失败: {e}", flush=True)
                    traceback.print_exc()

    db.commit()

    _log_op(db, int(user_id),
        action=Action.UPDATE,
        module=LogModule.QUOTATION,
        resource_type='quotation',
        resource_id=str(quotation.id),
        detail=f'归档报价单 "{quotation.name}"'
    )

    # 消息通知
    user_ids = [quotation.business_owner_id] if quotation.business_owner_id else []
    for mod in quotation.modules:
        for participant in mod.participants:
            if participant.user_id not in user_ids:
                user_ids.append(participant.user_id)

    if user_ids:
        _notify_users(db, user_ids,
            title='报价单版本更新',
            content=f'"{quotation.name}"已更新到v{version.version_no}版本',
            msg_type='version_updated',
            related_id=quotation.id,
            related_type='quotation'
        )

    return {
        'message': '归档成功',
        'quotation': quotation.to_dict(),
        'version': version.to_dict()
    }


@router.post("/quotations/{quotation_id}/unarchive")
def unarchive_quotation(
    quotation_id: int,
    db=Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    _check_permission(db, int(user_id), 'quotation.edit')
    quotation = db.query(Quotation).get(quotation_id)
    if not quotation:
        raise HTTPException(status_code=404, detail='报价单不存在')

    if quotation.status != 'approved':
        raise HTTPException(status_code=400, detail='报价单未归档')

    quotation.status = 'draft'

    if quotation.type == 'line':
        for child in quotation.children.all():
            if child.status == 'approved':
                child.status = 'draft'

    db.commit()

    _log_op(db, int(user_id),
        action=Action.UPDATE,
        module=LogModule.QUOTATION,
        resource_type='quotation',
        resource_id=str(quotation.id),
        detail=f'撤销归档 "{quotation.name}"'
    )

    return {
        'message': '撤销归档成功',
        'quotation': quotation.to_dict()
    }


# ---- 参与人员 ----

@router.get("/quotations/{quotation_id}/participants")
def get_participants(
    quotation_id: int,
    db=Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    participants = db.query(QuotationParticipant).filter_by(
        quotation_id=quotation_id).all()
    return JSONResponse(content=[p.to_dict() for p in participants], status_code=200)


@router.post("/quotations/{quotation_id}/participants")
def add_participant(
    quotation_id: int,
    body: ParticipantAdd,
    db=Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    _check_permission(db, int(user_id), 'quotation.edit')
    current_user = db.query(User).get(int(user_id))

    participant = QuotationParticipant(
        quotation_id=quotation_id,
        user_id=body.user_id,
        participant_type=body.participant_type
    )
    db.add(participant)
    db.commit()

    quotation = db.query(Quotation).get(quotation_id)
    added_user = db.query(User).get(body.user_id)
    if quotation and added_user and current_user:
        type_map = {
            'project': '项目', 'agency': '机构', 'electrical': '电气', 'engineer': '工程师'
        }
        type_label = type_map.get(body.participant_type, body.participant_type)
        _send_message(db, recipient_id=added_user.id,
            title='你已被添加为报价单参与人',
            content=f'你已被添加为"{quotation.name}"的{type_label}参与人，由{current_user.real_name}添加',
            msg_type='participant_added',
            related_id=quotation_id,
            related_type='quotation'
        )

    return JSONResponse(content=participant.to_dict(), status_code=201)


@router.put("/quotations/{quotation_id}/participants/{participant_user_id}")
def update_participant_type(
    quotation_id: int,
    participant_user_id: int,
    body: ParticipantUpdate,
    db=Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    _check_permission(db, int(user_id), 'quotation.edit')
    participant = db.query(QuotationParticipant).filter_by(
        quotation_id=quotation_id,
        user_id=participant_user_id
    ).first()
    if not participant:
        raise HTTPException(status_code=404, detail='参与人员不存在')
    participant.participant_type = body.participant_type
    db.commit()
    return JSONResponse(content=participant.to_dict(), status_code=200)


@router.delete("/quotations/{quotation_id}/participants/{participant_user_id}")
def remove_participant(
    quotation_id: int,
    participant_user_id: int,
    db=Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    _check_permission(db, int(user_id), 'quotation.edit')
    participant = db.query(QuotationParticipant).filter_by(
        quotation_id=quotation_id,
        user_id=participant_user_id
    ).first()
    if not participant:
        raise HTTPException(status_code=404, detail='参与人员不存在')
    db.delete(participant)
    db.commit()
    return JSONResponse(content={'message': '移除成功'}, status_code=200)


# ---- 复制 ----

@router.post("/quotations/{quotation_id}/copy")
def copy_quotation(
    quotation_id: int,
    db=Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    _check_permission(db, int(user_id), 'quotation.create')
    original = db.query(Quotation).get(quotation_id)
    if not original:
        raise HTTPException(status_code=404, detail='报价单不存在')

    uid = int(user_id)
    new_quotation = Quotation(
        name=f"{original.name} (副本)",
        type=original.type,
        scheme_no=original.scheme_no,
        status='draft',
        creator_id=uid,
        business_owner_id=original.business_owner_id
    )
    db.add(new_quotation)
    db.flush()

    # 复制模块
    original_modules = db.query(Module).filter_by(quotation_id=quotation_id).all()
    for mod in original_modules:
        new_module = Module(
            quotation_id=new_quotation.id,
            name=mod.name,
            code=mod.code
        )
        db.add(new_module)
        db.flush()

        original_materials = db.query(ModuleMaterial).filter_by(module_id=mod.id).all()
        for mm in original_materials:
            new_mm = ModuleMaterial(
                module_id=new_module.id,
                material_id=mm.material_id,
                quantity=mm.quantity,
                selected_by_id=uid
            )
            db.add(new_mm)

    # 复制其他费用
    original_fees = db.query(OtherFee).filter_by(quotation_id=quotation_id).all()
    for fee in original_fees:
        new_fee = OtherFee(
            quotation_id=new_quotation.id,
            module_id=fee.module_id,
            fee_type=fee.fee_type,
            location=fee.location,
            amount=fee.amount,
            description=fee.description
        )
        db.add(new_fee)

    db.commit()
    return JSONResponse(content=new_quotation.to_dict(), status_code=201)


# ---- 汇总 ----

@router.get("/quotations/{quotation_id}/summary")
def get_quotation_summary(
    quotation_id: int,
    db=Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    quotation = db.query(Quotation).get(quotation_id)
    if not quotation:
        raise HTTPException(status_code=404, detail='报价单不存在')

    is_line = quotation.type == 'line'

    if is_line:
        all_ids = [quotation_id] + [c.id for c in quotation.children.all()]
    else:
        all_ids = [quotation_id]

    # 费用系数
    if quotation.coefficients:
        fee_rates = quotation.coefficients
        default_rate = 1.0
    else:
        all_rates = db.query(FeeRate).all()
        fee_rates = {r.category: float(r.rate) for r in all_rates}
        default_rate = fee_rates.get('默认', 1.0)

    # 物料费用
    module_summaries = []
    total_material = 0.0
    total_with_rates = 0.0
    rate_details = {}

    for qid in all_ids:
        for module in db.query(Module).filter_by(quotation_id=qid).all():
            module_materials = db.query(ModuleMaterial).filter_by(module_id=module.id).all()
            module_amount = 0.0
            module_amount_with_rate = 0.0

            for mm in module_materials:
                if mm.is_other and mm.unit_price_override:
                    amount = float(mm.unit_price_override)
                    category = 'other'
                    rate = float(fee_rates.get('other', default_rate))
                elif mm.material:
                    amount = float(mm.material.unit_price) * float(mm.quantity)
                    category = mm.material.category or 'standard'
                    rate = float(fee_rates.get(category, default_rate))
                else:
                    continue

                module_amount += amount
                module_amount_with_rate += amount * rate

                if category not in rate_details:
                    rate_details[category] = {'base': 0, 'with_rate': 0, 'rate': rate}
                rate_details[category]['base'] += amount
                rate_details[category]['with_rate'] += amount * rate

            total_material += module_amount
            total_with_rates += module_amount_with_rate

            if is_line:
                child_q = db.query(Quotation).get(qid)
                source_name = child_q.name if qid != quotation_id else '线体本身'
            else:
                source_name = module.name

            module_summaries.append({
                'module_id': module.id,
                'module_name': module.name,
                'module_code': module.code,
                'source': source_name if is_line else None,
                'material_count': len(module_materials),
                'material_amount': round(module_amount, 2),
                'material_amount_with_rate': round(module_amount_with_rate, 2)
            })

    # 费用项（仅报价单自己的）
    total_fees = sum(float(f.amount or 0) for f in db.query(OtherFee).filter_by(
        quotation_id=quotation_id).all())

    # 人力
    total_labor = sum(float(l.total or 0) for l in db.query(LaborHour).filter(
        LaborHour.quotation_id.in_(all_ids)).all())

    # 包装
    packing_entries = db.query(PackingEntry).filter(
        PackingEntry.quotation_id.in_(all_ids)).all()
    total_packing = 0.0
    packing_details = []
    for entry in packing_entries:
        up = float(entry.unit_price) if entry.unit_price else (
            float(entry.packing_type.unit_price) if entry.packing_type and entry.packing_type.unit_price else 0)
        qty = float(entry.quantity or 0)
        sub = up * qty
        total_packing += sub
        packing_details.append({
            'packing_type_name': entry.packing_type.name if entry.packing_type else '',
            'unit_price': up,
            'quantity': qty,
            'total': round(sub, 2)
        })

    # 差旅人天
    person_days_entries = db.query(TravelPersonDays).filter(
        TravelPersonDays.quotation_id.in_(all_ids)).all()
    total_person_days = 0.0
    person_days_details = []
    for entry in person_days_entries:
        up = float(entry.unit_price) if entry.unit_price else (
            float(entry.travel_category.day_rates[0].unit_price)
            if entry.travel_category and entry.travel_category.day_rates else 0)
        pd_val = float(entry.person_days or 0)
        sub = up * pd_val
        total_person_days += sub
        person_days_details.append({
            'travel_category_name': entry.travel_category.name if entry.travel_category else '',
            'unit_price': up,
            'person_days': pd_val,
            'total': round(sub, 2)
        })

    # 差旅人次
    person_trip_entries = db.query(TravelPersonTrip).filter(
        TravelPersonTrip.quotation_id.in_(all_ids)).all()
    total_person_trips = 0.0
    person_trip_details = []
    for entry in person_trip_entries:
        subtotal = _calc_person_trip_total(db, entry)
        total_person_trips += subtotal
        if entry.unit_price or entry.visa_fee:
            up = float(entry.unit_price) if entry.unit_price else 0
            vf = float(entry.visa_fee) if entry.visa_fee else 0
        else:
            fee_record = db.query(TravelPersonTripFee).filter_by(
                travel_category_id=entry.travel_category_id,
                travel_mode_id=entry.travel_mode_id,
                is_active=True
            ).first()
            up = float(fee_record.unit_price or 0) if fee_record else 0
            vf = float(fee_record.visa_fee or 0) if fee_record else 0
        person_trip_details.append({
            'travel_category_name': f"{entry.travel_category.name if entry.travel_category else ''} {entry.travel_mode.name if entry.travel_mode else ''}",
            'person_count': float(entry.person_count or 0),
            'unit_price': up,
            'visa_fee': vf,
            'total': round(subtotal, 2)
        })

    # 汇总计算
    total_new_fees = total_packing + total_person_days + total_person_trips
    fees_total = total_fees + total_labor + total_new_fees
    subtotal = total_with_rates + fees_total
    profit_rate = float(quotation.profit_rate) if quotation.profit_rate else 0.0
    subtotal_with_profit = subtotal * (1 + profit_rate)
    tax_rate_val = float(quotation.tax_rate) if quotation.tax_rate else 0.0
    tax_amount = subtotal_with_profit * tax_rate_val
    grand_total = subtotal_with_profit + tax_amount

    return {
        'quotation': quotation.to_dict(),
        'is_line': is_line,
        'modules': module_summaries,
        'fees': [f.to_dict() for f in db.query(OtherFee).filter_by(quotation_id=quotation_id).all()],
        'material_total': round(total_material, 2),
        'material_total_with_rates': round(total_with_rates, 2),
        'fees_total': round(fees_total, 2),
        'fee_total': round(total_fees, 2),
        'labor_total': round(total_labor, 2),
        'fee_rates': fee_rates,
        'rate_details': [{'category': k, **v} for k, v in rate_details.items()],
        'packing_details': packing_details,
        'person_days_details': person_days_details,
        'person_trip_details': person_trip_details,
        'total_packing': round(total_packing, 2),
        'total_person_days': round(total_person_days, 2),
        'total_person_trips': round(total_person_trips, 2),
        'packing_total': round(total_packing, 2),
        'travel_person_days_total': round(total_person_days, 2),
        'travel_person_trips_total': round(total_person_trips, 2),
        'total_new_fees': round(total_new_fees, 2),
        'subtotal': round(subtotal, 2),
        'profit_rate': profit_rate,
        'subtotal_with_profit': round(subtotal_with_profit, 2),
        'tax_rate': tax_rate_val,
        'tax_amount': round(tax_amount, 2),
        'grand_total': round(grand_total, 2),
        'child_count': len(all_ids) - 1 if is_line else 0,
    }


