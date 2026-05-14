"""
迁移数据库 - 添加同步相关新字段
"""
from app import db
from run import app

def migrate_add_columns():
    """为 users 表添加新字段"""
    with app.app_context():
        conn = db.engine.connect()
        
        # 检查并添加 users 表新字段
        new_columns = [
            ('employee_id', 'BIGINT'),
            ('dept_id', 'BIGINT'),
            ('position_id', 'BIGINT'),
            ('sync_flag', 'BOOLEAN DEFAULT True'),
        ]
        
        for col_name, col_type in new_columns:
            try:
                conn.execute(db.text(f"ALTER TABLE users ADD COLUMN IF NOT EXISTS {col_name} {col_type}"))
                print(f"✓ users.{col_name} 已添加")
            except Exception as e:
                print(f"✗ users.{col_name} 失败: {e}")
        
        # 创建 departments 表
        try:
            db.create_all()
            print("✓ 新表创建成功")
        except Exception as e:
            print(f"✗ 创建表失败: {e}")
        
        conn.commit()
        conn.close()

if __name__ == '__main__':
    migrate_add_columns()
    print("迁移完成")
