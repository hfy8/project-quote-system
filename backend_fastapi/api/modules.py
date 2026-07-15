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
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import or_, text

from core.schemas import ModuleCreate, ModuleUpdate, ModuleMaterialAdd, ModuleMaterialUpdate
from core.auth import get_db, get_current_user_id
from api.quotations import _check_permission
from utils.log_helpers import record_crud, record_diff_update


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
        result = {
            "module_type": inferred,
            "module_type_label": MODULE_TYPE_LABELS.get(inferred, '其他'),
            "user_count": len(types),
            "source": "participant_types",
        }
    elif body.get('quotation_id'):
        # 推断的是"当前用户对该报价单的参与类型" (用于模块创建人场景)
        # 不是该报价单全部参与人混合 (那样 agency+project+electrical 永远是 other)
        from core.models.quotation import QuotationParticipant
        my_rows = db.query(QuotationParticipant.participant_type)\
            .filter(
                QuotationParticipant.quotation_id == body['quotation_id'],
                QuotationParticipant.user_id == int(user_id),
            )\
            .all()
        if not my_rows:
            result = {
                "module_type": "other",
                "module_type_label": "其他",
                "user_count": 0,
                "participant_type": None,
                "source": "quotation_id",
                "message": f"当前用户 (id={user_id}) 在该报价单无参与类型记录, 默认为: 其他",
            }
        else:
            # 一个 user 可能在该报价单有多种类型 (e.g. 同时是 agency + electrical)
            # 取主类型 (单一 → 直接用, 混合 → 兜底 other)
            types = [r[0] for r in my_rows]
            inferred = infer_module_type_from_participant_types(types)
            primary = types[0] if len(set(types)) == 1 else None
            result = {
                "module_type": inferred,
                "module_type_label": MODULE_TYPE_LABELS.get(inferred, '其他'),
                "user_count": len(types),
                "participant_type": primary,
                "source": "quotation_id",
            }
    elif body.get('user_ids'):
        inferred = infer_module_type_from_user_ids(db, body['user_ids'])
        result = {
            "module_type": inferred,
            "module_type_label": MODULE_TYPE_LABELS.get(inferred, '其他'),
            "user_count": len(body['user_ids']),
            "source": "user_ids",
        }
    else:
        # 兜底
        result = {
            "module_type": "other",
            "module_type_label": "其他",
            "user_count": 0,
            "source": "empty",
        }

    # 记录推断操作 (纯计算, 不写库, 记一条审计日志)
    record_crud(
        user_id, 'module', 'create',
        f'推断模块类型: {result.get("module_type")} (来源={result.get("source")}, 数量={result.get("user_count")})',
        resource_type='module',
    )
    return result


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

    record_crud(
        user_id, 'module', 'create',
        f'创建模块 {module.name} (代码={module.code or "-"}, 报价单ID={quotation_id})',
        resource_type='module', resource_id=str(module.id),
    )
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
    changed_fields = list(update_data.keys())
    for field, value in update_data.items():
        setattr(module, field, value)
    db.commit()

    # 记录字段变更日志 (模块名/代码变更附带上前后值, 便于审计)
    detail_suffix = ''
    if 'name' in update_data:
        detail_suffix += f': 名称 → {module.name}'
    if 'code' in update_data:
        detail_suffix += f', 代码 → {module.code or "-"}'
    record_diff_update(
        user_id, 'module', f'模块 {module.name} (ID={module.id})',
        changed_fields,
        resource_type='module', resource_id=str(module_id),
        detail_suffix=detail_suffix,
    )
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

    # 删除前快照 (delete 后对象会 expire)
    module_name = module.name
    module_code = module.code or "-"

    db.delete(module)
    db.commit()

    record_crud(
        user_id, 'module', 'delete',
        f'删除模块 {module_name} (代码={module_code}, ID={module_id})',
        resource_type='module', resource_id=str(module_id),
    )
    return {"message": "删除成功"}


@router.get("/modules/{module_id}/materials", summary="获取模块物料列表")
def get_module_materials(
    module_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(200, ge=1, le=500),
    sort_by: Optional[str] = Query(None, description="排序字段: material_name | specification | quantity | subtotal"),
    sort_order: Optional[str] = Query("asc", pattern="^(asc|desc)$", description="asc / desc"),
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    from core.models import ModuleMaterial, Material
    query = db.query(ModuleMaterial).filter_by(module_id=module_id)
    total = query.count()

    # 默认 + 显式排序: 物料名 → 规格 → id (稳定排序)
    if sort_by:
        col = {
            'material_name': Material.name,
            'specification': Material.spec,
            'quantity': ModuleMaterial.quantity,
            'subtotal': None,  # subtotal 是 to_dict 计算字段, 见下方
        }.get(sort_by)
        if col is not None:
            if sort_order == 'desc':
                col = col.desc()
            query = query.join(Material, ModuleMaterial.material_id == Material.id).order_by(col, ModuleMaterial.id)
    else:
        # 默认: 物料名升序 + 规格升序 + id (稳定排序)
        query = query.join(Material, ModuleMaterial.material_id == Material.id).order_by(
            Material.name.asc(),
            Material.spec.asc(),
            ModuleMaterial.id.asc()
        )

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
    from core.models import ModuleMaterial, Material, Module

    # 查询模块名 + 物料名 (用于日志, 提前获取避免后续 expire)
    mod_obj = db.query(Module).get(module_id)
    module_name = mod_obj.name if mod_obj else f"#{module_id}"
    material = db.query(Material).get(body.material_id)
    material_name = material.name if material else f"#{body.material_id}"
    material_unit = material.unit if material and material.unit else ""

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
        # 快照物料类型 (机械类/非机械类) — migration 017
        # 优先用前端传的, 没传则从 Material 表读, 都没有默认 'other'
        material_type=(body.material_type or (material.material_type if material else 'other') or 'other'),
    )
    db.add(mm)
    db.commit()

    record_crud(
        user_id, 'module', 'create',
        f'添加物料 {material_name} x {mm.quantity}{material_unit} (模块={module_name})',
        resource_type='module_material', resource_id=str(mm.id),
    )
    return mm.to_dict()


@router.put("/module_materials/{id}", summary="更新模块物料")
def update_module_material(
    id: int,
    body: ModuleMaterialUpdate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    _check_permission(db, int(user_id), 'module.edit')
    from core.models import ModuleMaterial, Material
    mm = db.query(ModuleMaterial).get(id)
    if not mm:
        raise HTTPException(status_code=404, detail="模块物料不存在")

    # 记录原值 (用于 audit 详情), 提前快照避免后续 expire
    old_quantity = mm.quantity
    old_material_id = mm.material_id
    old_unit_price_override = mm.unit_price_override
    old_module_id = mm.module_id

    update_data = body.model_dump(exclude_unset=True)
    changed_fields = []
    for field, value in update_data.items():
        # 特殊处理：is_other 时改 unit_price_override
        if field == "unit_price_override" and not mm.is_other:
            continue
        changed_fields.append(field)
        setattr(mm, field, value)
    db.commit()

    # 记录字段变更日志
    if changed_fields:
        # 取模块名/物料名
        from core.models import Module
        mod_obj = db.query(Module).get(old_module_id)
        module_name = mod_obj.name if mod_obj else f"#{old_module_id}"
        mat_obj = db.query(Material).get(mm.material_id)
        material_name = mat_obj.name if mat_obj else f"#{mm.material_id}"

        detail_suffix = ''
        if 'quantity' in changed_fields:
            detail_suffix += f': 数量 {old_quantity}→{mm.quantity}'
        if 'unit_price_override' in changed_fields:
            old_p = old_unit_price_override if old_unit_price_override is not None else "-"
            new_p = mm.unit_price_override if mm.unit_price_override is not None else "-"
            detail_suffix += f', 单价 {old_p}→{new_p}'
        if 'material_id' in changed_fields and old_material_id != mm.material_id:
            detail_suffix += f', 物料ID {old_material_id}→{mm.material_id}'

        record_diff_update(
            user_id, 'module', f'模块物料 {material_name} (模块={module_name}, ID={id})',
            changed_fields,
            resource_type='module_material', resource_id=str(id),
            detail_suffix=detail_suffix,
        )
    return mm.to_dict()


@router.delete("/module_materials/{id}", summary="从模块移除物料")
def remove_module_material(
    id: int,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    _check_permission(db, int(user_id), 'module.edit')
    from core.models import ModuleMaterial, Material, Module
    mm = db.query(ModuleMaterial).get(id)
    if not mm:
        raise HTTPException(status_code=404, detail="模块物料不存在")

    # 删除前快照 (避免后续 expire)
    module_id = mm.module_id
    material_id = mm.material_id
    mod_obj = db.query(Module).get(module_id)
    module_name = mod_obj.name if mod_obj else f"#{module_id}"
    mat_obj = db.query(Material).get(material_id)
    material_name = mat_obj.name if mat_obj else f"#{material_id}"

    db.delete(mm)
    db.commit()

    record_crud(
        user_id, 'module', 'delete',
        f'移除物料 {material_name} (模块={module_name}, ID={id})',
        resource_type='module_material', resource_id=str(id),
    )
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


@router.get("/quotations/all-modules", summary="全局模块列表（分页，跨报价单）")
def get_all_modules_paginated(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
    exclude_quotation_id: Optional[int] = Query(None, description="排除的报价单 ID（一般是当前正在编辑的）"),
    quotation_id: Optional[int] = Query(None, description="兼容旧调用：等同于 exclude_quotation_id"),
    keyword: Optional[str] = Query(None, description="按模块名/报价单名模糊搜索"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(15, ge=1, le=100, description="每页条数"),
):
    """跨报价单全局模块列表（供"从其他报价单复制模块"弹窗使用）

    权限规则: 任何登录用户都可调用。
    返回的模块来自 "用户有权限看到的报价单" 范围内的模块（按 admin 看到所有，普通用户仅看参与的）。
    排除 exclude_quotation_id（当前正在编辑的报价单）。
    按 module 字段、报价单 name 字段做模糊搜索。
    """
    from core.models import Module, Quotation, QuotationParticipant, User
    from sqlalchemy import or_

    excluded = exclude_quotation_id if exclude_quotation_id is not None else quotation_id
    uid = int(user_id)
    user = db.query(User).get(uid)
    if not user:
        raise HTTPException(status_code=401, detail='用户不存在')

    # admin: 全部报价单的模块
    # 普通用户: 仅其参与或 business_owner 的报价单的模块
    base_query = db.query(Module).join(Quotation, Module.quotation_id == Quotation.id)
    if user.role != 'admin':
        base_query = base_query.outerjoin(
            QuotationParticipant,
            (QuotationParticipant.quotation_id == Quotation.id) &
            (QuotationParticipant.user_id == uid)
        ).filter(
            or_(
                QuotationParticipant.user_id == uid,
                Quotation.business_owner_id == uid,
            )
        )

    if excluded is not None:
        base_query = base_query.filter(Module.quotation_id != excluded)

    if keyword:
        kw = f"%{keyword.strip()}%"
        base_query = base_query.filter(
            or_(
                Module.name.like(kw),
                Module.name_en.like(kw),
                Module.code.like(kw),
                Quotation.name.like(kw),
                Quotation.scheme_no.like(kw),
            )
        )

    total = base_query.count()
    modules = base_query.order_by(Module.created_at.desc()) \
        .offset((page - 1) * page_size) \
        .limit(page_size) \
        .all()

    # 批量取 quotation 信息（避免 N+1）
    q_ids = list({m.quotation_id for m in modules})
    quotations = {q.id: q for q in db.query(Quotation).filter(Quotation.id.in_(q_ids)).all()} if q_ids else {}

    items = []
    for mod in modules:
        mod_dict = mod.to_dict()
        q = quotations.get(mod.quotation_id)
        mod_dict['quotation_name'] = q.name if q else f"报价单{mod.quotation_id}"
        mod_dict['quotation_scheme_no'] = q.scheme_no if q else None
        items.append(mod_dict)

    return JSONResponse(content={
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
    }, status_code=200)


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

    # 记录批量复制操作日志
    module_names = ', '.join(c['source_module_name'] for c in copied)
    total_materials = sum(c['materials_count'] for c in copied)
    record_crud(
        user_id, 'module', 'create',
        f'从报价单 #{source_qid} 复制 {len(copied)} 个模块 [{module_names}] 到报价单 #{quotation_id} (共 {total_materials} 个物料)',
        resource_type='module',
        resource_id=f'batch-{source_qid}->{quotation_id}',
    )

    return {
        "success": True,
        "target_quotation_id": quotation_id,
        "source_quotation_id": source_qid,
        "copied": copied,
        "total_copied": len(copied),
        "total_materials": sum(c["materials_count"] for c in copied),
    }