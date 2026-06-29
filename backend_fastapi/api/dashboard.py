"""FastAPI 路由 - 首页 Dashboard 统计

一次返回首页所有需要的数据, 减少首页请求次数
"""
from datetime import datetime, timedelta
from collections import Counter
from fastapi import APIRouter, Depends

from core.auth import get_db, get_current_user_id
from core.models.quotation import Quotation
from core.models.material import Material
from core.models.change_request import ChangeRequest
from core.models.archive_approval import ArchiveApproval
from core.models.message import Message

router = APIRouter(prefix="/api/dashboard")


@router.get("/stats")
def get_dashboard_stats(
    db=Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    """首页 dashboard 一次性返回:
    - 报价单统计 (总数 / 各状态 / 本月新增)
    - 物料统计 (总数 / 按分类)
    - 待审批任务 (归档审批 + 变更申请 + 未读消息)
    - 最近 7 天报价单趋势 (每天新增数 + 审批通过数)
    """
    uid = int(user_id)
    now = datetime.utcnow()
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    seven_days_ago = now - timedelta(days=7)

    # ===== 1. 报价单统计 (admin 看全局, 其他用户看参与的) =====
    # 获取总数 (SQLAlchemy ORM count)
    total = db.query(Quotation).filter(Quotation.parent_id.is_(None)).count()
    # 各状态
    status_rows = db.query(Quotation.status, Quotation.id).filter(Quotation.parent_id.is_(None)).all()
    status_count = Counter(r.status for r in status_rows)
    by_status = {
        'draft': status_count.get('draft', 0),
        'approved': status_count.get('approved', 0),
        'approved_pending': status_count.get('approved_pending', 0),  # 待归档审批
        'archived': status_count.get('archived', 0),
        'rejected': status_count.get('rejected', 0),
    }
    # 本月新增
    monthly_new = db.query(Quotation).filter(
        Quotation.parent_id.is_(None),
        Quotation.created_at >= month_start
    ).count()

    # ===== 2. 物料统计 =====
    materials_total = db.query(Material).count()
    # 按分类统计
    cat_rows = db.query(Material.category).all()
    cat_counter = Counter(r.category for r in cat_rows)
    materials_by_category = {
        'large': cat_counter.get('large', 0),      # 大件
        'standard': cat_counter.get('standard', 0), # 核心部件
        'other': cat_counter.get('other', 0),       # 其他件
    }

    # ===== 3. 我的待办 =====
    # 3.1 待审批归档 (我是审批人 且 status=pending)
    pending_archives = db.query(ArchiveApproval).filter_by(
        approver_id=uid, status='pending'
    ).count()
    # 3.2 待审变更申请 (如果参与了该报价单的变更审核)
    pending_changes = db.query(ChangeRequest).filter_by(status='pending').count()
    # 3.3 未读消息
    unread_messages = db.query(Message).filter_by(recipient_id=uid, is_read=False).count()

    # ===== 4. 最近 7 天趋势 (每天新增报价单数) =====
    recent_q = db.query(
        Quotation.id,
        Quotation.status,
        Quotation.created_at
    ).filter(
        Quotation.parent_id.is_(None),
        Quotation.created_at >= seven_days_ago
    ).all()
    # 按天聚合
    daily_new = {}
    daily_approved = {}
    for q in recent_q:
        day = q.created_at.strftime('%m-%d') if q.created_at else None
        if not day:
            continue
        daily_new[day] = daily_new.get(day, 0) + 1
        if q.status in ('approved', 'archived'):
            daily_approved[day] = daily_approved.get(day, 0) + 1
    # 补齐最近 7 天 (没数据的天数补 0)
    trend = []
    for i in range(7):
        d = (now - timedelta(days=6 - i)).strftime('%m-%d')
        trend.append({
            'date': d,
            'new': daily_new.get(d, 0),
            'approved': daily_approved.get(d, 0),
        })

    return {
        'quotations': {
            'total': total,
            'by_status': by_status,
            'monthly_new': monthly_new,
        },
        'materials': {
            'total': materials_total,
            'by_category': materials_by_category,
        },
        'my_tasks': {
            'pending_archives': pending_archives,    # 待审批归档数
            'pending_changes': pending_changes,      # 待审变更申请数
            'unread_messages': unread_messages,      # 未读消息数
        },
        'trend': trend,                              # 最近 7 天趋势
    }
