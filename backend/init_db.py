"""
初始化数据库并创建默认管理员用户
"""
from app import create_app, db
from app.models import User


def init_db():
    """初始化数据库"""
    app = create_app()
    with app.app_context():
        # 创建所有表
        db.create_all()

        # 创建默认管理员用户
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                real_name='管理员',
                role='admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)

            # 创建默认业务用户
            business = User(
                username='business',
                real_name='业务人员',
                role='business'
            )
            business.set_password('123456')
            db.session.add(business)

            db.session.commit()
            print('数据库初始化完成，默认用户已创建:')
            print('  - admin / admin123 (管理员)')
            print('  - business / 123456 (业务人员)')
        else:
            print('数据库已存在，跳过初始化')


if __name__ == '__main__':
    init_db()