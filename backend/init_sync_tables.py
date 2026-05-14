"""
创建新的数据同步相关表
"""
from app import db
from app.models import Department, Position, Organization, Employee

def create_sync_tables():
    """创建同步数据表"""
    db.create_all()
    print("新表创建成功: departments, positions, organizations, employees")

def init_default_admin():
    """初始化默认管理员账号（如果不存在）"""
    from app.models import User
    from werkzeug.security import generate_password_hash
    
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            password_hash=generate_password_hash('admin123'),
            real_name='系统管理员',
            role='admin',
            is_active=True,
            sync_flag=False  # 标记为非同步账号
        )
        db.session.add(admin)
        db.session.commit()
        print("默认管理员账号创建成功: admin/admin123")
    else:
        print("管理员账号已存在")

if __name__ == '__main__':
    from run import app
    with app.app_context():
        create_sync_tables()
        init_default_admin()
