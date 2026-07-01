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
from api.quotations import _check_permission


def error_response(message: str, status_code: int):
    """返回与 Flask 一致的 {'error': ...} 格式（兼容旧前端）"""
    return JSONResponse(status_code=status_code, content={"error": message})


router = APIRouter()


# ============== 端点 ==============

@router.post("/modules/infer-type", summary="根据参与人员类型推断模块类型")
def infer_module_type(
    body: dict,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """
    前端传入以下任一参数:
    - user_ids: 用户 ID 列表 (后端会查 quotation_participants 表)
    - participant_types: 直接传参与类型列表 (前端已知类型时直接传, 不需后端再查)
    - quotation_id: 直接用报价单 ID, 查所有参与人员的类型

    推断规则 (使用 QuotationParticipant.participant_type):
    - 全部 agency → mechanical (机构)
    - 全部 electrical → electrical (电气)
    - 混合 / project / 空 → other (其他)
    """
    from core.models.module import (
        infer_module_type_from_participant_types,
        infer_module_type_from_user_ids,
        MODULE_TYPE_LABELS,
    )

    # 优先级: participant_types > quotation_id > user_ids
    if body.get('participant_types') is not None:
        types = body['participant_types'] or []
        inferred = infer_module_type_from_participant_types(types)
        return {
            "module_type": inferred,
            "module_type_label": MODULE_TYPE_LABELS.get(inferred, '其他'),
            "user_count": len(types),
            "source": "participant_types",
        }
    if body.get('quotation_id'):
        from core.models.quotation import QuotationParticipant
        rows = db.query(QuotationParticipant.participant_type)\
            .filter(QuotationParticipant.quotation_id == body['quotation_id'])\
            .all()
        types = [r[0] for r in rows]
        inferred = infer_module_type_from_participant_types(types)
        return {
            "module_type": inferred,
            "module_type_label": MODULE_TYPE_LABELS.get(inferred, '其他'),
            "user_count": len(types),
            "source": "quotation_id",
        }
    if body.get('user_ids'):
        inferred = infer_module_type_from_user_ids(db, body['user_ids'])
        return {
            "module_type": inferred,
            "module_type_label": MODULE_TYPE_LABELS.get(inferred, '其他'),
            "user_count": len(body['user_ids']),
            "source": "user_ids",
        }
    # 兜底
    return {
        "module_type": "other",
        "module_type_label": "其他",
        "user_count": 0,
        "source": "empty",
    }


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
    _check_permission(db, int(user_id), 'module.create')
    from core.models import Module, User, QuotationParticipant
    from core.models.module import (
        MODULE_TYPE_OTHER, MODULE_TYPE_CHOICES, infer_module_type_from_user_ids,
    )
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

    # module_type 处理: 优先用请求 body 显式值, 否则默认 other
    module_type = (body.module_type or MODULE_TYPE_OTHER).lower() if hasattr(body, 'module_type') else MODULE_TYPE_OTHER
    if module_type not in MODULE_TYPE_CHOICES:
        module_type = MODULE_TYPE_OTHER

    module = Module(
        quotation_id=quotation_id,
        name=body.name,
        name_en=body.name_en,
        code=body.code,
        description=body.description,
        module_type=module_type,
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
    _check_permission(db, int(user_id), 'module.edit')
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
    _check_permission(db, int(user_id), 'module.delete')
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
    _check_permission(db, int(user_id), 'module.edit')
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
    _check_permission(db, int(user_id), 'module.edit')
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
    _check_permission(db, int(user_id), 'module.edit')
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


# ============== 复制模块（从其他报价单）==============
@router.post("/quotations/{quotation_id}/copy-modules", summary="从源报价单复制模块到当前报价单")
def copy_modules_from_quotation(
    quotation_id: int,
    body: dict,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    _check_permission(db, int(user_id), 'module.create')
    """
    从指定源报价单复制模块到当前报价单（事务内一次性完成）。

    Body:
        {
            "source_quotation_id": int,   # 源报价单 ID
            "module_ids": [int, ...]      # 要复制的模块 ID 列表
        }

    逻辑:
        1. 校验权限: 同 create_module 规则 (module.create OR 是参与人)
        2. 校验源报价单存在
        3. 校验所有 module_id 都属于源报价单
        4. 对每个模块:
           - 新建 Module (同名, code 同名, 描述同名)
           - 复制所有 ModuleMaterial (quantity, unit_price_override, is_other 全部带过去)
        5. 提交事务, 返回新模块列表

    Returns:
        {"copied": [{"new_module_id": N, "source_module_id": M, "materials_count": K}, ...]}
    """
    from core.models import Module, ModuleMaterial, Quotation, User, QuotationParticipant
    from utils.permissions import has_permission

    # 参数解析
    source_qid = body.get('source_quotation_id')
    module_ids = body.get('module_ids', [])

    if not source_qid or not isinstance(source_qid, int):
        raise HTTPException(status_code=400, detail="source_quotation_id 必填且为整数")
    if not module_ids or not isinstance(module_ids, list) or not all(isinstance(x, int) for x in module_ids):
        raise HTTPException(status_code=400, detail="module_ids 必填且为整数列表")

    if source_qid == quotation_id:
        raise HTTPException(status_code=400, detail="源报价单不能与目标报价单相同")

    # 权限检查 (1:1 复刻 create_module)
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="用户不存在")
    if not has_permission(user.role, "module.create"):
        participant = db.query(QuotationParticipant).filter_by(
            quotation_id=quotation_id, user_id=user_id
        ).first()
        if not participant:
            raise HTTPException(status_code=403, detail="没有权限")

    # 校验源报价单
    source_q = db.query(Quotation).get(source_qid)
    if not source_q:
        raise HTTPException(status_code=404, detail=f"源报价单 #{source_qid} 不存在")

    # 校验目标报价单
    target_q = db.query(Quotation).get(quotation_id)
    if not target_q:
        raise HTTPException(status_code=404, detail=f"目标报价单 #{quotation_id} 不存在")

    # 校验所有 module_ids 都属于源报价单
    source_modules = db.query(Module).filter(
        Module.id.in_(module_ids),
        Module.quotation_id == source_qid,
    ).all()
    found_ids = {m.id for m in source_modules}
    missing = set(module_ids) - found_ids
    if missing:
        raise HTTPException(
            status_code=400,
            detail=f"模块 {sorted(missing)} 不属于源报价单 #{source_qid}",
        )

    # 复制 (单事务)
    try:
        copied = []
        for src_mod in source_modules:
            # 1. 新建模块
            new_mod = Module(
                quotation_id=quotation_id,
                name=src_mod.name,
                name_en=src_mod.name_en,
                code=src_mod.code,
                description=src_mod.description,
            )
            db.add(new_mod)
            db.flush()  # 拿到 new_mod.id

            # 2. 复制物料
            materials_count = 0
            for src_mm in src_mod.materials:
                new_mm = ModuleMaterial(
                    module_id=new_mod.id,
                    material_id=src_mm.material_id,
                    is_other=src_mm.is_other,
                    quantity=src_mm.quantity,
                    unit_price_override=src_mm.unit_price_override,
                    selected_by_id=user_id,  # 当前用户作为选人
                )
                db.add(new_mm)
                materials_count += 1

            copied.append({
                "source_module_id": src_mod.id,
                "source_module_name": src_mod.name,
                "new_module_id": new_mod.id,
                "new_module_name": new_mod.name,
                "materials_count": materials_count,
            })

        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"复制失败: {str(e)}")

    # 失效缓存
    try:
        from core.services.cache import cache_invalidate_prefix
        cache_invalidate_prefix('quotations:list:')
    except Exception:
        pass

    return {
        "success": True,
        "target_quotation_id": quotation_id,
        "source_quotation_id": source_qid,
        "copied": copied,
        "total_copied": len(copied),
        "total_materials": sum(c["materials_count"] for c in copied),
    }