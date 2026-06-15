"""FastAPI 路由 - Modules (迁移版)

业务逻辑 1:1 复刻 backend/app/routes/modules.py

注意路径映射 (Flask module_bp 注册到 /api 蓝本):
- GET/POST /quotations/<id>/modules
- GET/PUT/DELETE /modules/<id>
- GET/POST /modules/<id>/materials
- PUT/DELETE /module_materials/<id>
- GET /modules/<id>/summary
- GET /quotations/<id>/all-modules (线体聚合)

FastAPI 用 include_router prefix='/api' + 完整路径
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import or_, text

from core.schemas import ModuleCreate, ModuleUpdate, ModuleMaterialAdd, ModuleMaterialUpdate
from core.auth import get_db, get_current_user_id


def error_response(message: str, status_code: int):
    """返回与 Flask 一致的 {'error': ...} 格式（兼容旧前端）"""
    return JSONResponse(status_code=status_code, content={"error": message})


router = APIRouter()


# ============== 端点 ==============

@router.get("/quotations/{quotation_id}/modules", summary="获取报价单的模块列表")
def get_modules(
    quotation_id: int,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """获取某报价单下所有模块"""
    from core.models import Module
    modules = db.query(Module).filter_by(quotation_id=quotation_id).all()
    return [m.to_dict() for m in modules]


@router.post("/quotations/{quotation_id}/modules", summary="创建模块", status_code=201)
def create_module(
    quotation_id: int,
    body: ModuleCreate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """创建模块 (1:1 复刻 Flask 权限逻辑)

    权限规则:
    - 有 module.create 权限的可以建
    - 否则必须是该报价单的参与人
    """
    from core.models import Module, User, QuotationParticipant
    from utils.permissions import has_permission

    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="用户不存在")

    # 权限检查 (1:1 复刻)
    if not has_permission(user.role, "module.create"):
        participant = db.query(QuotationParticipant).filter_by(
            quotation_id=quotation_id, user_id=user_id
        ).first()
        if not participant:
            raise HTTPException(status_code=403, detail="没有权限")

    module = Module(
        quotation_id=quotation_id,
        name=body.name,
        name_en=body.name_en,
        code=body.code,
        description=body.description,
    )
    db.add(module)
    db.commit()
    return module.to_dict()


@router.get("/modules/{module_id}", summary="获取模块详情")
def get_module(
    module_id: int,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    from core.models import Module
    module = db.query(Module).get(module_id)
    if not module:
        raise HTTPException(status_code=404, detail="模块不存在")
    return module.to_dict()


@router.put("/modules/{module_id}", summary="更新模块")
def update_module(
    module_id: int,
    body: ModuleUpdate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    from core.models import Module
    module = db.query(Module).get(module_id)
    if not module:
        raise HTTPException(status_code=404, detail="模块不存在")

    update_data = body.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(module, field, value)
    db.commit()
    return module.to_dict()


@router.delete("/modules/{module_id}", summary="删除模块")
def delete_module(
    module_id: int,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    from core.models import Module
    module = db.query(Module).get(module_id)
    if not module:
        raise HTTPException(status_code=404, detail="模块不存在")

    db.delete(module)
    db.commit()
    return {"message": "删除成功"}


@router.get("/modules/{module_id}/materials", summary="获取模块物料列表")
def get_module_materials(
    module_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(200, ge=1, le=500),
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    from core.models import ModuleMaterial
    query = db.query(ModuleMaterial).filter_by(module_id=module_id)
    total = query.count()
    materials = query.offset((page - 1) * page_size).limit(page_size).all()
    return {
        "items": [m.to_dict() for m in materials],
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@router.post("/modules/{module_id}/materials", summary="添加物料到模块", status_code=201)
def add_material_to_module(
    module_id: int,
    body: ModuleMaterialAdd,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """添加物料到模块 (1:1 复刻 Flask 的 '其他' 物料特殊逻辑)

    - 查 materials 表 name='其他' 的物料
    - 如果添加的是 '其他' 物料, 检查模块是否已添加过
    - quantity 固定为 1 (其他物料)
    """
    from core.models import ModuleMaterial

    # 查 '其他' 物料 ID
    other_material = db.execute(text(
        "SELECT id FROM materials WHERE name = '其他' LIMIT 1"
    )).fetchone()
    other_material_id = other_material[0] if other_material else None
    is_other = bool(other_material_id and body.material_id == other_material_id)

    if is_other:
        existing = db.execute(text('''
            SELECT id FROM module_materials
            WHERE module_id = :mid AND material_id = :mid2
            LIMIT 1
        '''), {"mid": module_id, "mid2": other_material_id}).fetchone()
        if existing:
            return error_response('该模块已添加"其他"物料，请直接修改其单价', 400)

    mm = ModuleMaterial(
        module_id=module_id,
        material_id=body.material_id,
        is_other=is_other,
        quantity=1 if is_other else body.quantity,
        unit_price_override=body.unit_price_override,
        selected_by_id=user_id,
    )
    db.add(mm)
    db.commit()
    return mm.to_dict()


@router.put("/module_materials/{id}", summary="更新模块物料")
def update_module_material(
    id: int,
    body: ModuleMaterialUpdate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    from core.models import ModuleMaterial
    mm = db.query(ModuleMaterial).get(id)
    if not mm:
        raise HTTPException(status_code=404, detail="模块物料不存在")

    update_data = body.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        # 特殊处理：is_other 时改 unit_price_override
        if field == "unit_price_override" and not mm.is_other:
            continue
        setattr(mm, field, value)
    db.commit()
    return mm.to_dict()


@router.delete("/module_materials/{id}", summary="从模块移除物料")
def remove_module_material(
    id: int,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    from core.models import ModuleMaterial
    mm = db.query(ModuleMaterial).get(id)
    if not mm:
        raise HTTPException(status_code=404, detail="模块物料不存在")

    db.delete(mm)
    db.commit()
    return {"message": "移除成功"}


@router.get("/modules/{module_id}/summary", summary="获取模块物料汇总")
def get_module_summary(
    module_id: int,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    from core.models import ModuleMaterial
    materials = db.query(ModuleMaterial).filter_by(module_id=module_id).all()

    total_quantity = sum(m.quantity for m in materials)
    total_amount = sum(
        float(m.unit_price_override) if m.is_other and m.unit_price_override
        else m.quantity * float(m.material.unit_price) if m.material and m.material.unit_price
        else 0
        for m in materials
    )

    return {
        "total_quantity": total_quantity,
        "total_amount": total_amount,
        "materials": [m.to_dict() for m in materials],
    }


@router.get("/quotations/{quotation_id}/all-modules", summary="线体报价单的所有子模块")
def get_all_modules(
    quotation_id: int,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """获取线体报价单的所有子报价单模块（聚合）

    与 summary 不同: 这里只是把所有模块聚合, 每个模块带 quotation_name
    """
    from core.models import Quotation, Module

    quotation = db.query(Quotation).get(quotation_id)
    if not quotation:
        raise HTTPException(status_code=404, detail="报价单不存在")

    child_ids = [c.id for c in quotation.children.all()]
    all_module_ids = [quotation_id] + child_ids
    modules = db.query(Module).filter(Module.quotation_id.in_(all_module_ids)).all()

    result = []
    for mod in modules:
        mod_dict = mod.to_dict()
        if mod.quotation_id == quotation_id:
            mod_dict["quotation_name"] = quotation.name + "（线体）"
        else:
            child_q = db.query(Quotation).get(mod.quotation_id)
            mod_dict["quotation_name"] = child_q.name if child_q else f"子报价单{mod.quotation_id}"
        result.append(mod_dict)

    return result