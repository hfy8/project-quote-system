"""FastAPI 路由 - Materials (迁移版)

业务逻辑 1:1 复刻 backend/app/routes/materials.py
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from core.schemas import MaterialCreate, MaterialUpdate
from core.auth import get_db, get_current_user_id


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
    from core.models import Material

    material = Material(
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
    from core.models import Material

    material = db.query(Material).get(material_id)
    if not material:
        raise HTTPException(status_code=404, detail="物料不存在")

    # Pydantic 只返回用户提供的字段(exclude_unset=True)
    update_data = body.model_dump(exclude_unset=True)
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