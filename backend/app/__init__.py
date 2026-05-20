from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS

db = SQLAlchemy()
jwt = JWTManager()
scheduler = None


def create_app():
    """Flask应用工厂"""
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    # 初始化扩展
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)

    # 注册蓝图
    from app.routes import auth_bp, quotation_bp, module_bp, material_bp, fee_bp, version_bp, user_bp, export_bp, logs_bp, roles_bp, fee_rate_bp, exchange_rate_bp, module_participant_bp, sync_bp, change_request_bp, messages_bp, labor_hours_bp, ptp_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(quotation_bp, url_prefix='/api/quotations')
    app.register_blueprint(module_bp, url_prefix='/api')
    app.register_blueprint(material_bp, url_prefix='/api/materials')
    app.register_blueprint(fee_bp, url_prefix='/api')
    app.register_blueprint(version_bp, url_prefix='/api')
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(export_bp, url_prefix='/api')
    app.register_blueprint(logs_bp, url_prefix='/api/logs')
    app.register_blueprint(roles_bp, url_prefix='/api/roles')
    app.register_blueprint(fee_rate_bp, url_prefix='/api/fee_rates')
    app.register_blueprint(exchange_rate_bp, url_prefix='/api/exchange_rates')
    app.register_blueprint(module_participant_bp, url_prefix='/api/modules')
    app.register_blueprint(sync_bp, url_prefix='/api/sync')
    app.register_blueprint(change_request_bp, url_prefix='/api/change-requests')
    app.register_blueprint(messages_bp, url_prefix='/api/messages')
    app.register_blueprint(labor_hours_bp, url_prefix='/api/quotations')
    app.register_blueprint(ptp_bp, url_prefix='/api/participant-type-permissions')

    # 初始化定时任务调度器
    from app.tasks import init_scheduler
    global scheduler
    scheduler = init_scheduler(app)

    return app
