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
    app.config.from_object('api_app.app.config.Config')

    # 初始化扩展
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)

    # 蓝图注册已迁移到 FastAPI 路由中

    # 初始化定时任务调度器（FastAPI 端已迁移到 lifespan 启动）
    # 通过环境变量 SKIP_FLASK_SCHEDULER=1 让 Flask 端不再启动，避免重复触发
    import os
    if not os.environ.get("SKIP_FLASK_SCHEDULER"):
        from api_app.app.tasks import init_scheduler
        global scheduler
        scheduler = init_scheduler(app)

    return app
