"""FastAPI 路由 - Materials (迁移版)

业务逻辑 1:1 复刻 backend/app/routes/materials.py
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from core.schemas import MaterialCreate, MaterialUpdate
from core.auth import get_db, get_current_user_id
from api.quotations import _check_permission
from utils.log_helpers import record_crud, record_diff_update, record_status_change


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
        material_type=body.material_type or 'other',  # migration 016
        status=body.status or "active",
    )
    db.add(material)
    db.commit()
    record_crud(
        user_id, 'material', 'create',
        f'创建物料 {material.name} (编码={material.item_no or "-"}, 分类={material.category or "-"})',
        resource_type='material', resource_id=str(material.id),
    )
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

    # 计算字段变更 (只跟踪任务指定的 5 个核心字段)
    tracked_fields = {'unit_price': 'price', 'name': 'name', 'category': 'category', 'spec': 'spec', 'unit': 'unit'}
    changed = []
    old_values = {}
    for field in tracked_fields:
        if field in update_data:
            new_val = update_data[field]
            old_val = getattr(material, field, None)
            if field == 'unit_price':
                # Numeric 比较
                old_cmp = float(old_val) if old_val is not None else 0
                new_cmp = float(new_val) if new_val is not None else 0
            else:
                old_cmp = old_val
                new_cmp = new_val
            if old_cmp != new_cmp:
                changed.append(tracked_fields[field])
                old_values[field] = (old_val, new_val)

    for field, value in update_data.items():
        setattr(material, field, value)

    db.commit()

    # 记录字段变更日志 (价格变更附带上价格前后值, 便于审计)
    detail_suffix = ''
    if 'unit_price' in changed and 'unit_price' in old_values:
        old_p, new_p = old_values['unit_price']
        detail_suffix = f': 价格 {old_p}→{new_p}'
    record_diff_update(
        user_id, 'material', f'物料 {material.name} (编码={material.item_no or "-"}, ID={material.id})',
        changed,
        resource_type='material', resource_id=str(material_id),
        detail_suffix=detail_suffix,
    )
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

    # 记录物料信息 (delete 后对象会被 expire, 提前捕获)
    material_name = material.name
    material_item_no = material.item_no or "-"

    db.delete(material)
    db.commit()
    record_crud(
        user_id, 'material', 'delete',
        f'删除物料 {material_name} (编码={material_item_no})',
        resource_type='material', resource_id=str(material_id),
    )
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
    record_status_change(
        user_id, 'material',
        f'物料 {material.name} (编码={material.item_no or "-"}, ID={material.id})',
        old_status='active' if material.status == 'inactive' else 'inactive',
        new_status=material.status,
        resource_type='material', resource_id=str(material_id),
    )
    return material.to_dict()


@router.post("/import", summary="批量导入物料", status_code=201)
def import_materials(
    materials_data: dict,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """批量导入物料 - 支持 upsert (品号去重/品名+规格联合去重)

    业务规则:
      1. 有品号且 DB 已存在 → UPDATE (更新全部字段)
      2. 有品号不存在, 但品名+规格已存在 → UPDATE
      3. 无品号, 但品名+规格已存在 → UPDATE
      4. 全新 → INSERT (有无品号均可)
    """
    _check_permission(db, int(user_id), 'material.create')
    from core.models import Material
    from sqlalchemy import and_

    # 前端发送格式: { materials: [...] }
    items = materials_data.get("materials", materials_data) if isinstance(materials_data, dict) else materials_data

    created = 0
    updated = 0
    skipped = 0
    errors = []

    for idx, m_data in enumerate(items):
        item_no = (m_data.get("item_no") or "").strip()

        try:
            existing = None
            # 1. 有品号 → 按品号查找
            if item_no:
                existing = db.query(Material).filter(Material.item_no == item_no).first()

            # 2. 品号不存在(或无品号) → 按品名+规格联合查找
            if not existing:
                name = (m_data.get("name") or "").strip()
                spec = (m_data.get("spec") or "").strip()
                if name and spec:
                    existing = db.query(Material).filter(
                        and_(
                            Material.name == name,
                            Material.spec == spec,
                        )
                    ).first()

            if existing:
                # UPDATE: 除 unit_price 外, 其他字段照常更新
                for field in ["name", "spec", "brand", "unit", "category", "status", "param1", "param2", "param3", "material_type"]:
                    if field in m_data and m_data[field] is not None:
                        setattr(existing, field, m_data[field])
                # 价格: 仅当 Excel 提供有效价格时才更新
                if "unit_price" in m_data and m_data["unit_price"] is not None:
                    existing.unit_price = m_data["unit_price"]
                # 确保 status 默认值
                if existing.status is None:
                    existing.status = "active"
                updated += 1
            else:
                # INSERT: Excel 有价格用 Excel 的, 否则默认 0
                price = m_data["unit_price"] if (m_data.get("unit_price") is not None) else 0
                material = Material(
                    name=m_data.get("name"),
                    spec=m_data.get("spec"),
                    brand=m_data.get("brand"),
                    unit=m_data.get("unit"),
                    unit_price=price,
                    category=m_data.get("category", "standard"),
                    material_type=m_data.get("material_type", "other"),  # migration 016
                    item_no=item_no or None,
                    param1=m_data.get("param1"),
                    param2=m_data.get("param2"),
                    param3=m_data.get("param3"),
                    status="active",
                )
                db.add(material)
                created += 1

        except Exception as e:
            errors.append({"index": idx, "item_no": item_no, "error": str(e)})
            db.rollback()
            # 重新开始一个新事务
            from sqlalchemy import text as sa_text
            db.execute(sa_text("ROLLBACK"))
            continue

    db.commit()

    # 操作日志: 记录批量导入结果
    total_count = created + updated
    success_count = total_count
    fail_count = len(errors)
    record_crud(
        user_id, 'material', 'import',
        f'导入物料 {success_count}/{total_count} 条 (创建 {created}, 更新 {updated}, 失败 {fail_count})',
        resource_type='material',
    )

    return {
        "created": created,
        "updated": updated,
        "skipped": skipped,
        "errors": errors,
        "total": created + updated,
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

    # 操作日志: 记录手动触发的价格同步
    n = result.get('total', 0) if isinstance(result, dict) else 0
    updated_n = result.get('updated', 0) if isinstance(result, dict) else 0
    failed_n = result.get('failed', 0) if isinstance(result, dict) else 0
    record_crud(
        current_user_id, 'material', 'update',
        f'触发物料价格同步 (dry_run={dry_run}, 范围={n}条, 更新={updated_n}, 失败={failed_n})',
        resource_type='material',
    )
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