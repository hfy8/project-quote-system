from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from app.tasks import trigger_sync_now
from app import create_app

sync_bp = Blueprint('sync', __name__)


@sync_bp.route('/trigger', methods=['POST'])
@jwt_required()
def trigger_sync():
    """手动触发数据同步"""
    try:
        app = create_app()
        trigger_sync_now(app)
        return jsonify({'message': '同步任务已触发，请查看日志获取同步结果'}), 200
    except Exception as e:
        return jsonify({'error': f'同步失败: {str(e)}'}), 500


@sync_bp.route('/status', methods=['GET'])
def sync_status():
    """获取同步任务状态"""
    return jsonify({
        'message': '定时同步任务已配置，每晚22:00自动执行',
        'schedule': '22:00 每日'
    }), 200
