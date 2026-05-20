import json
from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db, create_app
from app.models import Quotation, QuotationParticipant, User, Module, ModuleMaterial, OtherFee, FeeRate, VersionSnapshot, LaborHour, ParticipantTypePermission
from app.utils.permissions import check_permission, check_any_permission
from app.utils.logger import log_operation, log_operation_manual
from app.models.operation_log import Action, Module as LogModule
from app.routes.exports import generate_version_files
from app.services.message_service import MessageService

quotation_bp = Blueprint('quotations', __name__)


@quotation_bp.route('', methods=['GET'])
@jwt_required()
def get_quotations():
    """获取报价单列表，支持筛选和权限控制"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    query = Quotation.query

    # 普通用户只能看到自己参与的报价单，或自己负责的报价单
    if user.role != 'admin':
        query = query.outerjoin(QuotationParticipant).filter(
            db.or_(
                QuotationParticipant.user_id == user_id,
                Quotation.business_owner_id == user_id
            )
        )

    # 状态筛选
    status = request.args.get('status')
    if status:
        query = query.filter(Quotation.status == status)

    # 类型筛选
    qtype = request.args.get('type')
    if qtype:
        query = query.filter(Quotation.type == qtype)

    # 关键词搜索（名称或方案号）
    keyword = request.args.get('keyword')
    if keyword:
        query = query.filter(
            db.or_(
                Quotation.name.like(f'%{keyword}%'),
                Quotation.scheme_no.like(f'%{keyword}%')
            )
        )

    quotations = query.order_by(Quotation.created_at.desc()).all()
    return jsonify([q.to_dict() for q in quotations]), 200


@quotation_bp.route('', methods=['POST'])
@jwt_required()
@check_permission('quotation.create')
@check_any_permission('quotation.create', 'quotation.*')
def create_quotation():
    """创建报价单"""
    data = request.get_json()
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    quotation = Quotation(
        name=data.get('name'),
        type=data.get('type', 'single'),
        scheme_no=data.get('scheme_no'),
        status='draft',
        creator_id=user_id,
        business_owner_id=data.get('business_owner_id'),
        tax_rate=data.get('tax_rate', 0.13),
        profit_rate=data.get('profit_rate', 0.0),
        currency=data.get('currency', 'CNY')
    )
    db.session.add(quotation)
    db.session.commit()

    # 记录日志
    log_operation(
        action=Action.CREATE,
        module=LogModule.QUOTATION,
        resource_type='quotation',
        resource_id=quotation.scheme_no or str(quotation.id),
        detail=f'创建报价单 "{quotation.name}"'
    )

    return jsonify(quotation.to_dict()), 201


@quotation_bp.route('/<quotation_id>', methods=['GET'])
@jwt_required()
def get_quotation(quotation_id):
    """获取报价单详情 - 支持数字ID或方案号"""
    # 尝试用数字ID查询
    try:
        quotation = Quotation.query.get(int(quotation_id))
    except (ValueError, TypeError):
        quotation = None
    # 如果没找到，尝试用方案号查询
    if not quotation:
        quotation = Quotation.query.filter_by(scheme_no=quotation_id).first()
    if not quotation:
        return jsonify({'error': '报价单不存在'}), 404
    return jsonify(quotation.to_dict()), 200


@quotation_bp.route('/<quotation_id>/permissions', methods=['GET'])
@jwt_required()
def get_quotation_permissions(quotation_id):
    """获取当前用户对该报价单的操作权限（按参与人员类型）"""
    user_id = get_jwt_identity()
    try:
        quotation = Quotation.query.get(int(quotation_id))
    except (ValueError, TypeError):
        quotation = None
    if not quotation:
        return jsonify({'error': '报价单不存在'}), 404

    # 查找当前用户在报价单中的参与记录
    participant = QuotationParticipant.query.filter_by(
        quotation_id=quotation.id,
        user_id=user_id
    ).first()

# 如果是创建者（业务负责人），拥有全部权限（读 project 的全部 tab）
    if quotation.business_owner_id == user_id:
        all_tabs = [p.tab_name for p in ParticipantTypePermission.query.filter_by(
            participant_type='project', is_disabled=False).all()]
        return jsonify({
            'participant_type': 'owner',
            'can_edit_coefficients': True,
            'can_edit_participants': True,
            'can_edit_materials': True,
            'can_edit_modules': True,
            'can_edit_fees': True,
            'tabs': all_tabs
        }), 200

    # 如果不是参与人，仅能查看
    if not participant:
        return jsonify({
            'participant_type': None,
            'can_edit_coefficients': False,
            'can_edit_participants': False,
            'can_edit_materials': False,
            'can_edit_modules': False,
            'can_edit_fees': False,
            'tabs': ['summary']
        }), 200

    # 按参与类型从数据库读取可用 tab
    ptype = participant.participant_type
    perms = ParticipantTypePermission.query.filter_by(
        participant_type=ptype, is_disabled=False).order_by(
        ParticipantTypePermission.sort_order).all()
    tabs = [p.tab_name for p in perms]

    can_edit_materials = 'materials' in tabs
    can_edit_modules = 'modules' in tabs
    can_edit_fees = 'fees' in tabs
    can_edit_participants = 'participants' in tabs
    can_edit_coefficients = 'coefficients' in tabs

    return jsonify({
        'participant_type': ptype,
        'can_edit_coefficients': can_edit_coefficients,
        'can_edit_participants': can_edit_participants,
        'can_edit_materials': can_edit_materials,
        'can_edit_modules': can_edit_modules,
        'can_edit_fees': can_edit_fees,
        'tabs': tabs
    }), 200


@quotation_bp.route('/<quotation_id>', methods=['PUT'])
@jwt_required()
@check_permission('quotation.edit')
@check_any_permission('quotation.edit', 'quotation.*')
def update_quotation(quotation_id):
    """更新报价单"""
    quotation = Quotation.query.get(quotation_id)
    if not quotation:
        return jsonify({'error': '报价单不存在'}), 404

    data = request.get_json()
    quotation.name = data.get('name', quotation.name)
    quotation.type = data.get('type', quotation.type)
    quotation.scheme_no = data.get('scheme_no', quotation.scheme_no)
    quotation.business_owner_id = data.get('business_owner_id', quotation.business_owner_id)
    quotation.tax_rate = data.get('tax_rate', quotation.tax_rate)
    quotation.profit_rate = data.get('profit_rate', quotation.profit_rate)
    if 'currency' in data:
        quotation.currency = data.get('currency')
    if 'coefficients' in data:
        quotation.coefficients = data.get('coefficients')

    db.session.commit()
    return jsonify(quotation.to_dict()), 200


@quotation_bp.route('/<quotation_id>', methods=['DELETE'])
@jwt_required()
@check_permission('quotation.delete')
@check_any_permission('quotation.delete', 'quotation.*')
def delete_quotation(quotation_id):
    """删除报价单"""
    quotation = Quotation.query.get(quotation_id)
    if not quotation:
        return jsonify({'error': '报价单不存在'}), 404

    detail = f'删除报价单 "{quotation.name}" ({quotation.scheme_no or quotation.id})'
    db.session.delete(quotation)
    db.session.commit()

    # 记录日志
    log_operation(
        action=Action.DELETE,
        module=LogModule.QUOTATION,
        resource_type='quotation',
        resource_id=str(quotation.id),
        detail=detail
    )
    return jsonify({'message': '删除成功'}), 200


@quotation_bp.route('/<int:quotation_id>/status', methods=['PUT'])
@jwt_required()
@check_permission('quotation.edit')
def update_status(quotation_id):
    """更新报价单状态"""
    quotation = Quotation.query.get(quotation_id)
    if not quotation:
        return jsonify({'error': '报价单不存在'}), 404

    data = request.get_json()
    new_status = data.get('status', quotation.status)
    
    # 校验状态转换
    valid_transitions = {
        'draft': ['approved'],
        'approved': ['draft'],  # 允许撤销归档
    }
    
    if new_status not in ['draft', 'approved']:
        return jsonify({'error': '无效的状态'}), 400
    
    if new_status != quotation.status:
        if new_status not in valid_transitions.get(quotation.status, []):
            return jsonify({'error': f'不能从 {quotation.status} 转换到 {new_status}'}), 400
        
        old_status = quotation.status
        quotation.status = new_status
        db.session.commit()
        
        # 归档时创建版本快照
        if new_status == 'approved':
            _create_version_snapshot(quotation, get_jwt_identity(), 'archive', '归档发布')
            log_operation(
                action=Action.EDIT,
                module=LogModule.QUOTATION,
                resource_type='quotation',
                resource_id=str(quotation.id),
                detail=f'归档报价单 \"{quotation.name}\"'
            )
        else:
            log_operation(
                action=Action.EDIT,
                module=LogModule.QUOTATION,
                resource_type='quotation',
                resource_id=str(quotation.id),
                detail=f'撤销归档 \"{quotation.name}\"'
            )
    
    return jsonify(quotation.to_dict()), 200


def _create_version_snapshot(quotation, operator_id, operation_type, remark=None):
    """创建版本快照"""
    # 获取当前最大版本号
    max_version = db.session.query(db.func.max(VersionSnapshot.version_no)).filter_by(
        quotation_id=quotation.id
    ).scalar() or 0
    
    # 获取报价单完整数据
    modules = Module.query.filter_by(quotation_id=quotation.id).all()
    fees = OtherFee.query.filter_by(quotation_id=quotation.id).all()
    
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
            'name': m.name,
            'code': m.code,
            'materials': [{
                'material_id': mm.material_id,
                'quantity': float(mm.quantity),
                'selected_by_id': mm.selected_by_id,
                'category': mm.material.category if mm.material else 'standard'
            } for mm in ModuleMaterial.query.filter_by(module_id=m.id).all()]
        } for m in modules],
        'fees': [{
            'module_id': f.module_id,
            'fee_type': f.fee_type,
            'location': f.location,
            'amount': float(f.amount) if f.amount else 0,
            'description': f.description
        } for f in fees],
        'labor_hours': [{
            'name': l.name,
            'hours': float(l.hours) if l.hours else 0,
            'unit_price': float(l.unit_price) if l.unit_price else 0,
            'total': float(l.total) if l.total else 0
        } for l in LaborHour.query.filter_by(quotation_id=quotation.id).all()]
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
    db.session.add(version)
    db.session.flush()  # 获取 version.id
    
    # 保存需要的数据用于异步生成（避免 ORM 对象在 flush 后 detached）
    async_quotation_id = quotation.id
    async_snapshot_data = json.dumps(snapshot_data, ensure_ascii=False)
    async_version_no = new_version_no
    
    # 生成版本文件（异步，不阻塞响应）
    try:
        from threading import Thread
        
        def generate_files_async():
            try:
                app = create_app()
                with app.app_context():
                    # 在新 app context 中查询版本记录
                    ver = VersionSnapshot.query.filter_by(
                        quotation_id=async_quotation_id,
                        version_no=async_version_no
                    ).first()
                    if ver:
                        file_paths = generate_version_files(async_quotation_id, async_version_no, async_snapshot_data)
                        ver.word_file = file_paths.get('word')
                        ver.pdf_file = file_paths.get('pdf')
                        db.session.commit()
            except Exception as e:
                print(f"异步生成版本文件失败: {e}")
        
        thread = Thread(target=generate_files_async)
        thread.daemon = True
        thread.start()
    except Exception as e:
        print(f"启动文件生成线程失败: {e}")
    
    return version


@quotation_bp.route('/<int:quotation_id>/versions', methods=['GET'])
@jwt_required()
def get_versions(quotation_id):
    """获取报价单版本历史"""
    quotation = Quotation.query.get(quotation_id)
    if not quotation:
        return jsonify({'error': '报价单不存在'}), 404
    
    versions = VersionSnapshot.query.filter_by(quotation_id=quotation_id).order_by(
        VersionSnapshot.version_no.desc()
    ).all()
    
    return jsonify([v.to_dict() for v in versions]), 200


@quotation_bp.route('/<int:quotation_id>/versions/<int:version_no>', methods=['GET'])
@jwt_required()
def get_version_detail(quotation_id, version_no):
    """获取指定版本的详细信息"""
    version = VersionSnapshot.query.filter_by(
        quotation_id=quotation_id,
        version_no=version_no
    ).first()
    
    if not version:
        return jsonify({'error': '版本不存在'}), 404
    
    return jsonify({
        **version.to_dict(),
        'snapshot_data': json.loads(version.snapshot_data)
    }), 200


@quotation_bp.route('/<int:quotation_id>/archive', methods=['POST'])
@jwt_required()
@check_permission('quotation.edit')
def archive_quotation(quotation_id):
    """归档报价单（发布版本）"""
    quotation = Quotation.query.get(quotation_id)
    if not quotation:
        return jsonify({'error': '报价单不存在'}), 404
    
    if quotation.status == 'approved':
        return jsonify({'error': '报价单已经归档'}), 400
    
    data = request.get_json() or {}
    remark = data.get('remark', '归档发布')
    
    # 创建版本快照
    version = _create_version_snapshot(quotation, get_jwt_identity(), 'archive', remark)
    
    # 更新状态
    quotation.status = 'approved'
    db.session.commit()
    
    log_operation(
        action=Action.UPDATE,
        module=LogModule.QUOTATION,
        resource_type='quotation',
        resource_id=str(quotation.id),
        detail=f'归档报价单 "{quotation.name}"'
    )
    
    # 发送消息通知业务负责人和成员（版本更新）
    user_ids = [quotation.business_owner_id] if quotation.business_owner_id else []
    for mod in quotation.modules:
        for participant in mod.participants:
            if participant.user_id not in user_ids:
                user_ids.append(participant.user_id)
    
    if user_ids:
        MessageService.notify_version_updated(
            user_ids=user_ids,
            quotation_name=quotation.name,
            version_no=new_version_no,
            quotation_id=quotation.id
        )
    
    return jsonify({
        'message': '归档成功',
        'quotation': quotation.to_dict(),
        'version': version.to_dict()
    }), 200


@quotation_bp.route('/<int:quotation_id>/unarchive', methods=['POST'])
@jwt_required()
@check_permission('quotation.edit')
def unarchive_quotation(quotation_id):
    """撤销归档"""
    quotation = Quotation.query.get(quotation_id)
    if not quotation:
        return jsonify({'error': '报价单不存在'}), 404
    
    if quotation.status != 'approved':
        return jsonify({'error': '报价单未归档'}), 400
    
    quotation.status = 'draft'
    db.session.commit()
    
    log_operation(
        action=Action.UPDATE,
        module=LogModule.QUOTATION,
        resource_type='quotation',
        resource_id=str(quotation.id),
        detail=f'撤销归档 \"{quotation.name}\"'
    )
    
    return jsonify({
        'message': '撤销归档成功',
        'quotation': quotation.to_dict()
    }), 200


@quotation_bp.route('/<int:quotation_id>/participants', methods=['GET'])
@jwt_required()
def get_participants(quotation_id):
    """获取报价单参与人员"""
    participants = QuotationParticipant.query.filter_by(quotation_id=quotation_id).all()
    return jsonify([p.to_dict() for p in participants]), 200


@quotation_bp.route('/<int:quotation_id>/participants', methods=['POST'])
@jwt_required()
@check_permission('quotation.edit')
def add_participant(quotation_id):
    """添加报价单参与人员"""
    data = request.get_json()
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    participant = QuotationParticipant(
        quotation_id=quotation_id,
        user_id=data.get('user_id'),
        participant_type=data.get('participant_type', 'project')
    )
    db.session.add(participant)
    db.session.commit()

    # 发消息通知被添加的人
    quotation = Quotation.query.get(quotation_id)
    added_user = User.query.get(data.get('user_id'))
    if quotation and added_user and current_user:
        MessageService.notify_participant_added(
            user_id=added_user.id,
            quotation_name=quotation.name,
            participant_type=data.get('participant_type', 'project'),
            added_by_name=current_user.real_name,
            quotation_id=quotation_id
        )

    return jsonify(participant.to_dict()), 201


@quotation_bp.route('/<int:quotation_id>/participants/<int:user_id>', methods=['PUT'])
@jwt_required()
@check_permission('quotation.edit')
def update_participant_type(quotation_id, user_id):
    """更新报价单参与人员类型"""
    data = request.get_json()
    participant = QuotationParticipant.query.filter_by(
        quotation_id=quotation_id,
        user_id=user_id
    ).first()
    if not participant:
        return jsonify({'error': '参与人员不存在'}), 404
    participant.participant_type = data.get('participant_type', participant.participant_type)
    db.session.commit()
    return jsonify(participant.to_dict()), 200


@quotation_bp.route('/<int:quotation_id>/participants/<int:user_id>', methods=['DELETE'])
@jwt_required()
@check_permission('quotation.edit')
def remove_participant(quotation_id, user_id):
    """移除报价单参与人员"""
    participant = QuotationParticipant.query.filter_by(
        quotation_id=quotation_id,
        user_id=user_id
    ).first()

    if not participant:
        return jsonify({'error': '参与人员不存在'}), 404

    db.session.delete(participant)
    db.session.commit()
    return jsonify({'message': '移除成功'}), 200


@quotation_bp.route('/<int:quotation_id>/copy', methods=['POST'])
@jwt_required()
@check_permission('quotation.create')
def copy_quotation(quotation_id):
    """复制报价单"""
    original = Quotation.query.get(quotation_id)
    if not original:
        return jsonify({'error': '报价单不存在'}), 404

    user_id = get_jwt_identity()
    new_quotation = Quotation(
        name=f"{original.name} (副本)",
        type=original.type,
        scheme_no=original.scheme_no,
        status='draft',
        creator_id=user_id,
        business_owner_id=original.business_owner_id
    )
    db.session.add(new_quotation)
    db.session.flush()

    # 复制模块
    original_modules = Module.query.filter_by(quotation_id=quotation_id).all()
    for mod in original_modules:
        new_module = Module(
            quotation_id=new_quotation.id,
            name=mod.name,
            code=mod.code
        )
        db.session.add(new_module)
        db.session.flush()

        # 复制模块物料
        original_materials = ModuleMaterial.query.filter_by(module_id=mod.id).all()
        for mm in original_materials:
            new_mm = ModuleMaterial(
                module_id=new_module.id,
                material_id=mm.material_id,
                quantity=mm.quantity,
                selected_by_id=user_id
            )
            db.session.add(new_mm)

    # 复制其他费用
    original_fees = OtherFee.query.filter_by(quotation_id=quotation_id).all()
    for fee in original_fees:
        new_fee = OtherFee(
            quotation_id=new_quotation.id,
            module_id=fee.module_id,
            fee_type=fee.fee_type,
            location=fee.location,
            amount=fee.amount,
            description=fee.description
        )
        db.session.add(new_fee)

    db.session.commit()
    return jsonify(new_quotation.to_dict()), 201


@quotation_bp.route('/<int:quotation_id>/summary', methods=['GET'])
@jwt_required()
def get_quotation_summary(quotation_id):
    """获取报价单汇总数据（含费用系数和税率）"""
    quotation = Quotation.query.get(quotation_id)
    if not quotation:
        return jsonify({'error': '报价单不存在'}), 404

    modules = Module.query.filter_by(quotation_id=quotation_id).all()
    fees = OtherFee.query.filter_by(quotation_id=quotation_id).all()
    labor_hours = LaborHour.query.filter_by(quotation_id=quotation_id).all()

    # 获取费用系数（优先使用报价单私有系数，否则用全局配置）
    coeff = None
    if quotation.coefficients:
        coeff = quotation.coefficients
        fee_rates = coeff
        default_rate = 1.0
    else:
        fee_rates = {r.category: float(r.rate) for r in FeeRate.query.all()}
        default_rate = fee_rates.get('默认', 1.0)

    module_summaries = []
    total_material = 0
    total_with_rates = 0
    rate_details = {}

    for module in modules:
        module_materials = ModuleMaterial.query.filter_by(module_id=module.id).all()
        module_amount = 0
        module_amount_with_rate = 0

        for mm in module_materials:
            if mm.material:
                amount = float(mm.material.unit_price) * mm.quantity
                module_amount += amount
                
                # 获取物料分类对应的费用系数
                category = mm.material.category or 'standard'
                if quotation.coefficients:
                    rate = float(quotation.coefficients.get(category, 1.0))
                else:
                    rate = float(fee_rates.get(category, default_rate))
                amount_with_rate = amount * rate
                module_amount_with_rate += amount_with_rate
                
                # 累计各分类费用
                if category not in rate_details:
                    rate_details[category] = {'base': 0, 'with_rate': 0, 'rate': rate}
                rate_details[category]['base'] += amount
                rate_details[category]['with_rate'] += amount_with_rate

        total_material += module_amount
        total_with_rates += module_amount_with_rate

        module_summaries.append({
            'module_id': module.id,
            'module_name': module.name,
            'module_code': module.code,
            'material_count': len(module_materials),
            'material_amount': round(module_amount, 2),
            'material_amount_with_rate': round(module_amount_with_rate, 2)
        })

    total_fees = sum(float(f.amount or 0) for f in fees)
    total_labor = sum(float(l.total or 0) for l in labor_hours)
    fees_total = total_fees + total_labor  # 费用合计含人力工时
    subtotal = total_with_rates + fees_total
    profit_rate = float(quotation.profit_rate) if quotation.profit_rate else 0.0
    subtotal_with_profit = subtotal * (1 + profit_rate)
    tax_amount = subtotal_with_profit * (quotation.tax_rate or 0)
    grand_total = subtotal_with_profit + tax_amount

    return jsonify({
        'quotation': quotation.to_dict(),
        'modules': module_summaries,
        'fees': [f.to_dict() for f in fees],
        'material_total': round(total_material, 2),
        'material_total_with_rates': round(total_with_rates, 2),
        'fees_total': round(fees_total, 2),
        'labor_total': round(total_labor, 2),
        'labor_hours': [l.to_dict() for l in labor_hours],
        'fee_rates': fee_rates,
        'rate_details': [{'category': k, **v} for k, v in rate_details.items()],
        'subtotal': round(subtotal, 2),
        'profit_rate': profit_rate,
        'subtotal_with_profit': round(subtotal_with_profit, 2),
        'tax_rate': quotation.tax_rate or 0,
        'tax_amount': round(tax_amount, 2),
        'grand_total': round(grand_total, 2)
    }), 200


@quotation_bp.route('/my-assignments', methods=['GET'])
@jwt_required()
def get_my_assignments():
    """获取当前用户参与的报价单（按报价单级别参与）"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': '用户不存在'}), 401

    # 获取用户作为报价单参与人的所有报价单
    participant_records = QuotationParticipant.query.filter_by(user_id=user_id).all()

    result = []
    for p in participant_records:
        quotation = Quotation.query.get(p.quotation_id)
        if not quotation:
            continue

        # 获取该报价单的模块数量和物料数量
        module_count = Module.query.filter_by(quotation_id=quotation.id).count()
        material_count = db.session.query(db.func.count(ModuleMaterial.id)).join(Module).filter(
            Module.quotation_id == quotation.id
        ).scalar() or 0

        result.append({
            'quotation_id': quotation.id,
            'quotation_name': quotation.name,
            'quotation_scheme_no': quotation.scheme_no,
            'quotation_status': quotation.status,
            'participant_type': p.participant_type,
            'business_owner_name': quotation.business_owner.real_name if quotation.business_owner else None,
            'module_count': module_count,
            'material_count': material_count,
            'created_at': quotation.created_at.isoformat() if quotation.created_at else None,
        })

    return jsonify(result), 200


@quotation_bp.route('/my-assigned-modules', methods=['GET'])
@jwt_required()
def get_my_assigned_modules():
    """获取当前用户被分配的模块（作为模块参与者）【保留兼容】"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': '用户不存在'}), 401

    # 获取用户作为模块参与者的所有模块
    from app.models.module import ModuleParticipant, Module

    # 先获取用户参与的所有模块ID
    participant_records = ModuleParticipant.query.filter_by(user_id=user_id).all()
    module_ids = [p.module_id for p in participant_records]

    if not module_ids:
        return jsonify([]), 200

    # 获取这些模块的详情（包含所属报价单信息）
    modules = Module.query.filter(Module.id.in_(module_ids)).all()

    result = []
    for mod in modules:
        # 获取模块物料数量
        material_count = ModuleMaterial.query.filter_by(module_id=mod.id).count()

        # 获取报价单信息
        quotation = Quotation.query.get(mod.quotation_id)

        result.append({
            'id': mod.id,
            'module_name': mod.name,
            'module_code': mod.code,
            'quotation_id': mod.quotation_id,
            'quotation_name': quotation.name if quotation else None,
            'quotation_scheme_no': quotation.scheme_no if quotation else None,
            'quotation_status': quotation.status if quotation else None,
            'material_count': material_count
        })

    return jsonify(result), 200