"""FastAPI 路由 - 版本快照 (迁移版)"""

import json
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.models import VersionSnapshot, Quotation
from app.models.material import Material
from api_app.main import get_db, get_current_user_id

router = APIRouter(prefix='/api')


class VersionCreate(BaseModel):
    operation_type: str = 'manual'
    remark: Optional[str] = None


# ──────────────────────────────────────────────
# 1) 版本列表
# ──────────────────────────────────────────────

@router.get('/quotations/{quotation_id}/versions')
def get_versions(quotation_id: int, db=Depends(get_db)):
    """获取版本列表"""
    versions = (
        db.query(VersionSnapshot)
        .filter_by(quotation_id=quotation_id)
        .order_by(VersionSnapshot.version_no.desc())
        .all()
    )
    return JSONResponse(content=[v.to_dict() for v in versions])


# ──────────────────────────────────────────────
# 2) 手动创建版本
# ──────────────────────────────────────────────

@router.post('/quotations/{quotation_id}/versions', status_code=201)
def create_version(
    quotation_id: int,
    body: VersionCreate,
    db=Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    """创建版本快照"""
    # 获取下一个版本号
    last_version = (
        db.query(VersionSnapshot)
        .filter_by(quotation_id=quotation_id)
        .order_by(VersionSnapshot.version_no.desc())
        .first()
    )
    next_version = (last_version.version_no + 1) if last_version else 1

    # 构建快照数据
    quotation = db.query(Quotation).get(quotation_id)
    if not quotation:
        raise HTTPException(status_code=404, detail='报价单不存在')

    if quotation.business_owner and quotation.creator:
        snapshot_data = {
            'quotation': {
                'name': quotation.name,
                'type': quotation.type,
                'scheme_no': quotation.scheme_no,
                'tax_rate': quotation.tax_rate,
                'currency': quotation.currency,
                'business_owner_id': quotation.business_owner_id,
                'business_owner_name': quotation.business_owner.real_name if quotation.business_owner else None,
                'creator_id': quotation.creator_id,
                'creator_name': quotation.creator.real_name if quotation.creator else None,
            },
            'modules': [m.to_dict() for m in quotation.modules],
            'fees': [f.to_dict() for f in quotation.fees],
        }
    else:
        snapshot_data = {
            'quotation': {
                'name': getattr(quotation, 'name', None),
                'type': getattr(quotation, 'type', None),
                'scheme_no': getattr(quotation, 'scheme_no', None),
                'tax_rate': getattr(quotation, 'tax_rate', None),
                'currency': getattr(quotation, 'currency', None),
                'business_owner_id': getattr(quotation, 'business_owner_id', None),
                'business_owner_name': quotation.business_owner.real_name if quotation.business_owner else None,
                'creator_id': getattr(quotation, 'creator_id', None),
                'creator_name': quotation.creator.real_name if quotation.creator else None,
            },
            'modules': [m.to_dict() for m in quotation.modules],
            'fees': [f.to_dict() for f in quotation.fees],
        }

    version = VersionSnapshot(
        quotation_id=quotation_id,
        version_no=next_version,
        snapshot_data=json.dumps(snapshot_data, ensure_ascii=False),
        operation_type=body.operation_type,
        remark=body.remark,
        operator_id=int(user_id),
    )
    db.add(version)
    db.commit()
    return JSONResponse(content=version.to_dict(), status_code=201)


# ──────────────────────────────────────────────
# 3) 版本详情
# ──────────────────────────────────────────────

@router.get('/versions/{version_id}')
def get_version(version_id: int, db=Depends(get_db)):
    """获取版本详情"""
    version = db.query(VersionSnapshot).get(version_id)
    if not version:
        raise HTTPException(status_code=404, detail='版本不存在')

    snapshot = json.loads(version.snapshot_data)
    result = version.to_dict()
    # 确保快照数据包含 quotation, modules, fees 顶层结构
    # 旧格式: {name, type, modules, fees} - 需要包装
    # 新格式: {quotation, modules, fees} - 直接使用
    if 'quotation' not in snapshot:
        if 'modules' in snapshot or 'fees' in snapshot:
            # 旧格式：modules和fees在顶层，需要包装到quotation下
            snapshot = {
                'quotation': snapshot,
                'modules': snapshot.get('modules', []),
                'fees': snapshot.get('fees', []),
            }
        else:
            # 无法识别的格式
            snapshot = {'quotation': snapshot, 'modules': [], 'fees': []}
    result['snapshot_data'] = snapshot
    return JSONResponse(content=result)


# ──────────────────────────────────────────────
# 4) 版本对比（按 ID）
# ──────────────────────────────────────────────

@router.get('/versions/{version_id}/compare/{other_id}')
def compare_versions(version_id: int, other_id: int, db=Depends(get_db)):
    """对比两个版本"""
    version1 = db.query(VersionSnapshot).get(version_id)
    version2 = db.query(VersionSnapshot).get(other_id)

    if not version1 or not version2:
        raise HTTPException(status_code=404, detail='版本不存在')

    def normalize(snapshot):
        """统一快照数据格式：确保 {quotation, modules, fees, labor_hours, packing_entries, person_days_entries, person_trip_entries} 顶层结构"""
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

    v1_data = normalize(json.loads(version1.snapshot_data))
    v2_data = normalize(json.loads(version2.snapshot_data))

    # 补充物料详情（旧快照可能只有 material_id）
    material_cache = {}

    def enrich_material(mat_data):
        """为物料补充 name/spec/brand/unit_price"""
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

    v1_data['modules'] = [enrich_module(m) for m in v1_data.get('modules', [])]
    v2_data['modules'] = [enrich_module(m) for m in v2_data.get('modules', [])]

    # 计算汇总（使用报价单系数，与PDF一致）
    from app.routes.exports import calculate_version_totals
    v1_totals = calculate_version_totals(v1_data)
    v2_totals = calculate_version_totals(v2_data)

    return JSONResponse(content={
        'version1': v1_data,
        'version2': v2_data,
        'totals1': v1_totals,
        'totals2': v2_totals,
    })


# ──────────────────────────────────────────────
# 5) 同一报价单的两个版本对比（按 version_no）
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

    # 线体：合并子报价单同 version_no 的快照数据
    def merge_extra(data, extra_snapshots):
        if not extra_snapshots:
            return
        for es in extra_snapshots:
            es_data = normalize(json.loads(es.snapshot_data))
            for key in [
                'modules',
                'fees',
                'labor_hours',
                'packing_entries',
                'person_days_entries',
                'person_trip_entries',
            ]:
                data[key] = data.get(key, []) + es_data.get(key, [])

    merge_extra(v1_data, extra_snapshots_v1)
    merge_extra(v2_data, extra_snapshots_v2)

    v1_data['modules'] = [enrich_module(m) for m in v1_data.get('modules', [])]
    v2_data['modules'] = [enrich_module(m) for m in v2_data.get('modules', [])]

    from app.routes.exports import calculate_version_totals
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
