"""FastAPI 路由 - 首页 Dashboard 统计

一次返回首页所有需要的数据, 减少首页请求次数
"""
from datetime import datetime, timedelta
from collections import Counter, defaultdict
from fastapi import APIRouter, Depends

from core.auth import get_db, get_current_user_id
from core.models.quotation import Quotation, QuotationParticipant
from core.models.material import Material
from core.models.change_request import ChangeRequest
from core.models.archive_approval import ArchiveApproval
from core.models.message import Message
from core.models.user import User

router = APIRouter(prefix="/api/dashboard")


def _is_admin(db, user_id):
    user = db.query(User).filter_by(id=user_id).first()
    return user and user.role == 'admin'


@router.get("/stats")
def get_dashboard_stats(
    db=Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    """首页 dashboard 一次性返回:
    - 报价单统计 (总数 / 各状态 / 本月新增 / 本周新增)
    - 物料统计 (总数 / 按分类 / Top5常用物料)
    - 我的待办 (归档审批 + 变更申请 + 未读消息)
    - 最近 7 天报价单趋势
    - Top 5 客户 (admin) / 本周我的业绩 (其他用户)
    - 最近 3 条消息摘要
    """
    uid = int(user_id)
    now = datetime.utcnow()
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    week_start = now - timedelta(days=now.weekday())  # 本周一
    week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
    seven_days_ago = now - timedelta(days=7)

    is_admin = _is_admin(db, uid)

    # ===== 1. 报价单统计 =====
    total = db.query(Quotation).filter(Quotation.parent_id.is_(None)).count()
    status_rows = db.query(Quotation.status).filter(Quotation.parent_id.is_(None)).all()
    status_count = Counter(r.status for r in status_rows)
    by_status = {
        'draft': status_count.get('draft', 0),
        'approved': status_count.get('approved', 0),
        'approved_pending': status_count.get('approved_pending', 0),
        'archived': status_count.get('archived', 0),
        'rejected': status_count.get('rejected', 0),
    }
    monthly_new = db.query(Quotation).filter(
        Quotation.parent_id.is_(None),
        Quotation.created_at >= month_start
    ).count()
    weekly_new = db.query(Quotation).filter(
        Quotation.parent_id.is_(None),
        Quotation.created_at >= week_start
    ).count()

    # ===== 2. 物料统计 =====
    materials_total = db.query(Material).count()
    cat_rows = db.query(Material.category).all()
    cat_counter = Counter(r.category for r in cat_rows)
    materials_by_category = {
        'large': cat_counter.get('large', 0),
        'standard': cat_counter.get('standard', 0),
        'other': cat_counter.get('other', 0),
    }

    # ===== 3. 我的待办 =====
    pending_archives = db.query(ArchiveApproval).filter_by(
        approver_id=uid, status='pending'
    ).count()
    # 待审变更申请 - admin 看全部,其他人看自己参与或自己提交的
    if is_admin:
        pending_changes = db.query(ChangeRequest).filter_by(status='pending').count()
    else:
        # 我参与的报价单的变更
        my_q_ids = db.query(QuotationParticipant.quotation_id).filter_by(
            user_id=uid
        ).subquery()
        pending_changes = db.query(ChangeRequest).filter(
            ChangeRequest.status == 'pending',
            ChangeRequest.quotation_id.in_(my_q_ids)
        ).count()
    unread_messages = db.query(Message).filter_by(
        recipient_id=uid, is_read=False
    ).count()

    # ===== 4. 最近 7 天趋势 =====
    recent_q = db.query(
        Quotation.id, Quotation.status, Quotation.created_at
    ).filter(
        Quotation.parent_id.is_(None),
        Quotation.created_at >= seven_days_ago
    ).all()
    daily_new = {}
    daily_approved = {}
    for q in recent_q:
        day = q.created_at.strftime('%m-%d') if q.created_at else None
        if not day:
            continue
        daily_new[day] = daily_new.get(day, 0) + 1
        if q.status in ('approved', 'archived'):
            daily_approved[day] = daily_approved.get(day, 0) + 1
    trend = []
    for i in range(7):
        d = (now - timedelta(days=6 - i)).strftime('%m-%d')
        trend.append({
            'date': d,
            'new': daily_new.get(d, 0),
            'approved': daily_approved.get(d, 0),
        })

    # ===== 5. Top 5 客户 (admin 全局, 其他人 自己参与的) =====
    if is_admin:
        # 从 quotation.name 提取客户名 (按项目名分组)
        # 由于没有 customer 表, 用项目名前缀模拟客户
        # 实际: 我们用项目名作为客户标识, name 通常包含客户名
        recent_for_clients = db.query(
            Quotation.name, Quotation.id
        ).filter(
            Quotation.parent_id.is_(None),
            Quotation.created_at >= month_start
        ).limit(200).all()
        # 按 name 的前 8 个字作为客户分组 (简化处理)
        client_counter = Counter()
        client_ids = defaultdict(list)
        for r in recent_for_clients:
            key = r.name[:8] if r.name else '未知'
            client_counter[key] += 1
            client_ids[key].append(r.id)
        top_clients = []
        for name, cnt in client_counter.most_common(5):
            top_clients.append({
                'name': name,
                'count': cnt,
                'latest_id': client_ids[name][0],
            })
    else:
        # 普通用户: 我本月业绩
        my_q_ids = db.query(QuotationParticipant.quotation_id).filter_by(
            user_id=uid
        ).subquery()
        my_monthly = db.query(Quotation).filter(
            Quotation.parent_id.is_(None),
            Quotation.created_at >= month_start,
            Quotation.id.in_(my_q_ids)
        ).count()
        my_monthly_approved = db.query(Quotation).filter(
            Quotation.parent_id.is_(None),
            Quotation.created_at >= month_start,
            Quotation.id.in_(my_q_ids),
            Quotation.status.in_(['approved', 'archived'])
        ).count()
        my_participating = db.query(Quotation).filter(
            Quotation.parent_id.is_(None),
            Quotation.id.in_(my_q_ids)
        ).count()
        top_clients = [{
            'name': '我参与的',
            'count': my_participating,
            'latest_id': None,
        }, {
            'name': '我本月新增',
            'count': my_monthly,
            'latest_id': None,
        }, {
            'name': '我本月通过',
            'count': my_monthly_approved,
            'latest_id': None,
        }]

    # ===== 6. 最近 3 条消息 =====
    recent_msgs = db.query(Message).filter_by(
        recipient_id=uid
    ).order_by(Message.created_at.desc()).limit(3).all()
    recent_messages = []
    for m in recent_msgs:
        recent_messages.append({
            'id': m.id,
            'title': m.title,
            'type': m.type,
            'is_read': m.is_read,
            'created_at': m.created_at.isoformat() if m.created_at else None,
            'related_id': m.related_id,
            'related_type': m.related_type,
            'sender_name': m.sender.real_name if m.sender else '系统',
        })

    # ===== 7. 本周业绩 (admin) / 部门分布 =====
    weekly_summary = {}
    if is_admin:
        weekly_summary['new'] = weekly_new
        weekly_summary['approved'] = db.query(Quotation).filter(
            Quotation.parent_id.is_(None),
            Quotation.status.in_(['approved', 'archived']),
            Quotation.updated_at >= week_start
        ).count()

    return {
        'quotations': {
            'total': total,
            'by_status': by_status,
            'monthly_new': monthly_new,
            'weekly_new': weekly_new,
        },
        'materials': {
            'total': materials_total,
            'by_category': materials_by_category,
        },
        'my_tasks': {
            'pending_archives': pending_archives,
            'pending_changes': pending_changes,
            'unread_messages': unread_messages,
        },
        'trend': trend,
        'top_clients': top_clients,
        'recent_messages': recent_messages,
        'weekly_summary': weekly_summary,
        'user_role': 'admin' if is_admin else 'business',
    }