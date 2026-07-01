"""FastAPI 路由 - Materials (迁移版)

业务逻辑 1:1 复刻 backend/app/routes/materials.py
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from core.schemas import MaterialCreate, MaterialUpdate
from core.auth import get_db, get_current_user_id
from api.quotations import _check_permission


router = APIRouter()


# ============== 异常 ==============
class NotFoundError(Exception):
    def __init__(self, message):
        self.message = message
        self.code = 404


class BadRequestError(Exception):
    def __init__(self, message):
        self.message = message
        self.code = 400


# ============== 端点(行为与 Flask 路由 1:1) ==============

@router.get("", summary="获取物料列表")
def get_materials(
    keyword: str = Query("", description="搜索关键词(名称/规格/品牌)"),
    category: str = Query(None, description="物料分类:large/standard/other"),
    status: str = Query(None, description="状态:active/inactive"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(50, ge=1, le=200, description="每页条数"),
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """获取物料列表(与 Flask 路由 1:1)"""
    from core.models import Material

    query = db.query(Material)
    if keyword:
        keyword_filter = f"%{keyword}%"
        query = query.filter(
            or_(
                Material.name.ilike(keyword_filter),
                Material.spec.ilike(keyword_filter),
                Material.brand.ilike(keyword_filter),
            )
        )
    if category:
        query = query.filter_by(category=category)
    if status:
        query = query.filter_by(status=status)

    total = query.count()
    materials = (
        query.order_by(Material.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return {
        "items": [m.to_dict() for m in materials],
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@router.post("", summary="创建物料", status_code=201)
def create_material(
    body: MaterialCreate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """创建物料(行为 1:1)"""
    _check_permission(db, int(user_id), 'material.create')
    from core.models import Material

    material = Material(
        item_no=(body.item_no or '').strip() or None,  # 品号, 空字符串转 None
        name=body.name,
        spec=body.spec,
        brand=body.brand,
        unit=body.unit,
        unit_price=body.unit_price,
        category=body.category,
        status=body.status or "active",
    )
    db.add(material)
    db.commit()
    return material.to_dict()


@router.put("/{material_id}", summary="更新物料")
def update_material(
    material_id: int,
    body: MaterialUpdate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """更新物料(行为 1:1)"""
    _check_permission(db, int(user_id), 'material.edit')
    from core.models import Material

    material = db.query(Material).get(material_id)
    if not material:
        raise HTTPException(status_code=404, detail="物料不存在")

    # Pydantic 只返回用户提供的字段(exclude_unset=True)
    update_data = body.model_dump(exclude_unset=True)
    # 品号空字符串归一为 None (允许没有品号)
    if 'item_no' in update_data and update_data['item_no'] is not None:
        update_data['item_no'] = (update_data['item_no'] or '').strip() or None
    for field, value in update_data.items():
        setattr(material, field, value)

    db.commit()
    return material.to_dict()


@router.delete("/{material_id}", summary="删除物料")
def delete_material(
    material_id: int,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """删除物料(行为 1:1:先删 module_materials 关联记录,再删物料)"""
    _check_permission(db, int(user_id), 'material.delete')
    from core.models import Material, ModuleMaterial

    material = db.query(Material).get(material_id)
    if not material:
        raise HTTPException(status_code=404, detail="物料不存在")

    # 先删除关联的 module_materials 记录
    db.query(ModuleMaterial).filter_by(material_id=material_id).delete()

    db.delete(material)
    db.commit()
    return {"message": "删除成功"}


@router.put("/{material_id}/toggle", summary="启用/禁用物料")
def toggle_material(
    material_id: int,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """切换 active/inactive 状态"""
    _check_permission(db, int(user_id), 'material.edit')
    from core.models import Material

    material = db.query(Material).get(material_id)
    if not material:
        raise HTTPException(status_code=404, detail="物料不存在")

    material.status = "inactive" if material.status == "active" else "active"
    db.commit()
    return material.to_dict()


@router.post("/import", summary="批量导入物料", status_code=201)
def import_materials(
    materials_data: list[dict],
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """批量导入物料

    兼容 Flask 版本的请求格式:{"materials": [...]} 或直接传 list
    """
    _check_permission(db, int(user_id), 'material.create')
    from core.models import Material

    # 兼容两种入参:dict 或 list
    if isinstance(materials_data, dict) and "materials" in materials_data:
        items = materials_data["materials"]
    else:
        items = materials_data

    created = []
    for m_data in items:
        material = Material(
            name=m_data.get("name"),
            spec=m_data.get("spec"),
            brand=m_data.get("brand"),
            unit=m_data.get("unit"),
            unit_price=m_data.get("unit_price", 0),
            category=m_data.get("category", "standard"),
            status="active",
        )
        db.add(material)
        created.append(material)

    db.commit()
    return {
        "created": len(created),
        "materials": [m.to_dict() for m in created],
    }


# ============== 价格同步 (定时任务 + 手动触发) ==============

@router.post("/sync-prices")
def sync_prices_endpoint(
    dry_run: bool = Query(False, description="只统计不写库"),
    batch_size: int = Query(50, description="每批 commit 数量"),
    current_user_id: int = Depends(get_current_user_id),
):
    """手动触发原材料价格同步 (通过品号查外部 API 更新 unit_price)

    默认每日 02:00 自动执行, 此接口用于:
      - 调试验证逻辑
      - 紧急刷新 (新接入了一批物料, 等不到 02:00)
      - 大批量价格变更后立即同步
    """
    import logging
    logger = logging.getLogger("api-materials")

    # 权限校验: 仅 admin 可触发
    from core.auth import get_db
    db = next(get_db())
    try:
        from core.models.user import User
        user = db.query(User).filter_by(id=current_user_id).first()
        if not user or user.role != "admin":
            raise HTTPException(status_code=403, detail="仅管理员可触发价格同步")
    finally:
        db.close()

    from core.tasks.material_price_sync import sync_material_prices
    logger.info(f"Manual sync triggered by user_id={current_user_id}, dry_run={dry_run}")
    result = sync_material_prices(batch_size=batch_size, dry_run=dry_run)
    return result


@router.get("/sync-prices/status")
def sync_prices_status(current_user_id: int = Depends(get_current_user_id)):
    """查看最近一次价格同步的状态 (任何登录用户可看)"""
    from db import db_session_factory
    from core.models.material import Material
    from sqlalchemy import func

    db = db_session_factory()
    try:
        # 统计各状态的物料数
        status_counts = dict(
            db.query(Material.last_price_sync_status, func.count(Material.id))
            .group_by(Material.last_price_sync_status)
            .all()
        )

        # 最近一次同步时间
        latest = db.query(func.max(Material.last_price_synced_at)).scalar()

        # 最近一次成功同步的物料
        latest_success = db.query(Material).filter(
            Material.last_price_sync_status == "success"
        ).order_by(Material.last_price_synced_at.desc()).first()

        return {
            "total_materials_with_item_no": db.query(Material).filter(
                Material.item_no.isnot(None),
                Material.item_no != "",
            ).count(),
            "sync_status_counts": {k or "never_synced": v for k, v in status_counts.items()},
            "latest_sync_at": latest.isoformat() + "Z" if latest else None,
            "latest_success_material": {
                "id": latest_success.id,
                "name": latest_success.name,
                "item_no": latest_success.item_no,
                "unit_price": float(latest_success.unit_price),
                "synced_at": latest_success.last_price_synced_at.isoformat() + "Z" if latest_success.last_price_synced_at else None,
            } if latest_success else None,
        }
    finally:
        db.close()