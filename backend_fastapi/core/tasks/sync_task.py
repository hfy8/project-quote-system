"""
数据同步任务 - 从 rs-pro-manage (SQL Server) 同步部门、人员等数据到报价系统
"""
import logging
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

logger = logging.getLogger(__name__)

# SQL Server 数据源配置
SQLSERVER_CONFIG = {
    'host': '192.168.100.70',
    'port': 1433,
    'database': 'RSHRIS',
    'username': 'sa',
    'password': 'Kayang123#',
    'charset': 'utf8'
}

# 部门数据 SQL
DEPT_SQL = """
    SELECT 
        "DepID" AS dept_id,
        "Title" AS dept_name,
        "AdminID" AS parent_id,
        "DepType" AS dept_type,
        "Remark" AS dept_desc,
        "DepCode" AS dept_code,
        "CompID" AS org_id,
        "DepGrade" AS dept_level,
        "innID" AS parent_path,
        CASE 
            WHEN "DepGrade" = 1 THEN "Director2"
            WHEN "DepGrade" = 2 THEN "Director"
            WHEN "DepGrade" = 3 THEN "Director3"
            ELSE NULL
        END AS header_id
    FROM oDepartment
    WHERE isDisabled = 0 OR isDisabled IS NULL
    ORDER BY DepGrade, AdminID, DepID
"""

# 人员数据 SQL
EMPLOYEE_SQL = """
    SELECT 
        "EID" AS employee_id,
        "Badge" AS employee_no,
        "Name" AS cn_name,
        "EName" AS en_name,
        "Name" AS nick_name,
        "DepID" AS dept_id,
        "CompID" AS org_id,
        "JobID" AS position_id,
        "Gender" AS gender,
        "email" AS email,
        "Mobile" AS mobile,
        "LeaveType" AS leave_type,
        "LeaveDate" AS leave_date
    FROM eEmployee
    WHERE "LeaveType" IS NULL AND "LeaveDate" IS NULL
"""

# 组织数据 SQL (skycompany 表)
ORG_SQL = """
    SELECT 
        "CompID" AS org_id,
        "CompCode" AS org_code,
        "CompName" AS org_name,
        "ParentID" AS parent_id
    FROM skycompany
"""

# 职位数据 SQL
POSITION_SQL = """
    SELECT 
        "JobID" AS position_id,
        "JobCode" AS position_code,
        "Title" AS position_name,
        "Remark" AS position_desc,
        "JobGrade" AS position_level,
        "JobType" AS position_type
    FROM oJob
"""


def get_sqlserver_connection():
    """获取 SQL Server 连接"""
    import pymssql
    return pymssql.connect(
        server=SQLSERVER_CONFIG['host'],
        port=SQLSERVER_CONFIG['port'],
        database=SQLSERVER_CONFIG['database'],
        user=SQLSERVER_CONFIG['username'],
        password=SQLSERVER_CONFIG['password'],
        charset=SQLSERVER_CONFIG['charset']
    )


def sync_departments():
    """同步部门数据"""
    from db import db
    from core.models import Department
    
    logger.info("开始同步部门数据...")
    conn = None
    cursor = None
    try:
        conn = get_sqlserver_connection()
        cursor = conn.cursor(as_dict=True)
        cursor.execute(DEPT_SQL)
        
        # 先标记所有部门为未同步
        Department.query.update({Department.sync_flag: False})
        db.session.commit()
        
        count = 0
        for row in cursor:
            dept = Department.query.filter_by(id=row['dept_id']).first()
            if dept:
                dept.name = row['dept_name']
                dept.code = row['dept_code']
                dept.description = row['dept_desc']
                dept.level = row['dept_level']
                dept.parent_id = row['parent_id']
                dept.parent_path = row['parent_path']
                dept.org_id = row['org_id']
                dept.dept_type = row['dept_type']
                dept.header_id = row['header_id']
                dept.sync_flag = True
            else:
                dept = Department(
                    id=row['dept_id'],
                    name=row['dept_name'],
                    code=row['dept_code'],
                    description=row['dept_desc'],
                    level=row['dept_level'],
                    parent_id=row['parent_id'],
                    parent_path=row['parent_path'],
                    org_id=row['org_id'],
                    dept_type=row['dept_type'],
                    header_id=row['header_id'],
                    sync_flag=True
                )
                db.session.add(dept)
            count += 1
            
            if count % 200 == 0:
                db.session.flush()
        
        # 删除未同步的部门
        Department.query.filter_by(sync_flag=False).delete()
        db.session.commit()
        logger.info(f"部门同步完成，共 {count} 条")
        
    except Exception as e:
        logger.error(f"部门同步失败: {e}")
        db.session.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def sync_organizations():
    """同步组织数据"""
    from db import db
    from core.models import Organization
    
    logger.info("开始同步组织数据...")
    conn = None
    cursor = None
    try:
        conn = get_sqlserver_connection()
        cursor = conn.cursor(as_dict=True)
        cursor.execute(ORG_SQL)
        
        Organization.query.update({Organization.sync_flag: False})
        db.session.commit()
        
        count = 0
        for row in cursor:
            org = Organization.query.filter_by(id=row['org_id']).first()
            if org:
                org.name = row['org_name']
                org.code = row['org_code']
                org.sync_flag = True
            else:
                org = Organization(
                    id=row['org_id'],
                    name=row['org_name'],
                    code=row['org_code'],
                    sync_flag=True
                )
                db.session.add(org)
            count += 1
            
            if count % 200 == 0:
                db.session.flush()
        
        Organization.query.filter_by(sync_flag=False).delete()
        db.session.commit()
        logger.info(f"组织同步完成，共 {count} 条")
        
    except Exception as e:
        logger.error(f"组织同步失败: {e}")
        db.session.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def sync_positions():
    """同步职位数据"""
    from db import db
    from core.models import Position
    
    logger.info("开始同步职位数据...")
    conn = None
    cursor = None
    try:
        conn = get_sqlserver_connection()
        cursor = conn.cursor(as_dict=True)
        cursor.execute(POSITION_SQL)
        
        Position.query.update({Position.sync_flag: False})
        db.session.commit()
        
        count = 0
        for row in cursor:
            pos = Position.query.filter_by(id=row['position_id']).first()
            if pos:
                pos.name = row['position_name']
                pos.code = row['position_code']
                pos.position_type = row['position_type']
                pos.sync_flag = True
            else:
                pos = Position(
                    id=row['position_id'],
                    name=row['position_name'],
                    code=row['position_code'],
                    position_type=row['position_type'],
                    sync_flag=True
                )
                db.session.add(pos)
            count += 1
            
            if count % 200 == 0:
                db.session.flush()
        
        Position.query.filter_by(sync_flag=False).delete()
        db.session.commit()
        logger.info(f"职位同步完成，共 {count} 条")
        
    except Exception as e:
        logger.error(f"职位同步失败: {e}")
        db.session.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def sync_employees():
    """同步员工数据"""
    from db import db
    from core.models import Employee, User
    
    logger.info("开始同步员工数据...")
    conn = None
    cursor = None
    try:
        conn = get_sqlserver_connection()
        cursor = conn.cursor(as_dict=True)
        cursor.execute(EMPLOYEE_SQL)
        
        Employee.query.update({Employee.sync_flag: False})
        db.session.commit()
        
        # 性别映射: SQL Server 1=男, 0=女 → 我们用 1=男, 0=女
        gender_map = {1: 1, 0: 0}  # 直接保持一致
        
        count = 0
        for row in cursor:
            emp = Employee.query.filter_by(id=row['employee_id']).first()
            
            # 性别转换
            gender = row['gender']
            if gender == 1:
                gender = 1  # 男
            elif gender == 0:
                gender = 0  # 女
            else:
                gender = None
            
            if emp:
                emp.employee_no = row['employee_no']
                emp.cn_name = row['cn_name']
                emp.en_name = row['en_name']
                emp.nick_name = row['nick_name']
                emp.gender = gender
                emp.email = row['email']
                emp.mobile = row['mobile']
                emp.dept_id = row['dept_id']
                emp.org_id = row['org_id']
                emp.position_id = row['position_id']
                emp.sync_flag = True
            else:
                emp = Employee(
                    id=row['employee_id'],
                    employee_no=row['employee_no'],
                    cn_name=row['cn_name'],
                    en_name=row['en_name'],
                    nick_name=row['nick_name'],
                    gender=gender,
                    email=row['email'],
                    mobile=row['mobile'],
                    dept_id=row['dept_id'],
                    org_id=row['org_id'],
                    position_id=row['position_id'],
                    sync_flag=True
                )
                db.session.add(emp)
            count += 1
            
            if count % 200 == 0:
                db.session.flush()
        
        Employee.query.filter_by(sync_flag=False).delete()
        db.session.commit()
        logger.info(f"员工同步完成，共 {count} 条")
        
    except Exception as e:
        logger.error(f"员工同步失败: {e}")
        db.session.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def sync_users_from_employees():
    """从员工数据同步用户到 users 表，并关联员工ID"""
    from db import db
    from core.models import User, Employee
    from werkzeug.security import generate_password_hash
    
    logger.info("开始同步用户数据...")
    
    try:
        # 标记所有非admin用户为未同步
        User.query.filter(User.username != 'admin').update({User.sync_flag: False})
        db.session.commit()
        
        # 找出所有有用户账号的员工
        employees = Employee.query.filter(
            Employee.employee_no.isnot(None),
            Employee.is_active == True
        ).all()
        
        count = 0
        for emp in employees:
            # 查找是否已有用户账号
            user = User.query.filter_by(username=emp.employee_no).first()
            
            if not user:
                # 创建新用户
                user = User(
                    username=emp.employee_no,
                    password_hash=generate_password_hash('123456'),  # 默认密码
                    real_name=emp.cn_name,
                    role='business',  # 默认角色
                    employee_id=emp.id,
                    dept_id=emp.dept_id,
                    position_id=emp.position_id,
                    is_active=True,
                    sync_flag=True
                )
                db.session.add(user)
            else:
                # 更新已有用户
                user.real_name = emp.cn_name
                user.employee_id = emp.id
                user.dept_id = emp.dept_id
                user.position_id = emp.position_id
                user.sync_flag = True
            
            count += 1
            
            if count % 200 == 0:
                db.session.flush()
        
        # 标记来自员工同步的用户为不活跃（但保留admin）
        User.query.filter(
            User.employee_id.isnot(None),
            User.sync_flag == False,
            User.username != 'admin'
        ).update({User.is_active: False})
        
        db.session.commit()
        logger.info(f"用户同步完成，共 {count} 条")
        
    except Exception as e:
        logger.error(f"用户同步失败: {e}")
        db.session.rollback()


def sync_all():
    """执行全部同步任务"""
    logger.info("=" * 50)
    logger.info("开始执行数据同步任务...")
    logger.info("=" * 50)
    
    try:
        sync_organizations()
        sync_departments()
        sync_positions()
        sync_employees()
        sync_users_from_employees()
        
        logger.info("=" * 50)
        logger.info("数据同步任务执行完成!")
        logger.info("=" * 50)
    except Exception as e:
        logger.error(f"同步任务执行失败: {e}")


def init_scheduler():
    """初始化定时任务调度器"""
    scheduler = BackgroundScheduler()
    
    # 每天晚上 10 点执行同步
    scheduler.add_job(
        func=sync_all,
        trigger=CronTrigger(hour=22, minute=0),
        id='daily_sync',
        name='每日数据同步',
        replace_existing=True
    )

    # 每天凌晨 3 点清理过期消息
    scheduler.add_job(
        func=cleanup_expired_messages,
        trigger=CronTrigger(hour=3, minute=0),
        id='message_cleanup',
        name='清理过期消息',
        replace_existing=True
    )
    
    # 也可以添加手动触发的任务（通过 API）
    scheduler.start()
    logger.info("定时任务调度器已启动，每晚22:00执行数据同步")
    
    return scheduler


# 手动触发同步的函数
def trigger_sync_now(app):
    """手动立即执行同步"""
    sync_all(app)


def cleanup_expired_messages():
    """清理过期消息"""
    from db import db
    from core.models import Message
    from datetime import datetime, timedelta
    
    try:
        read_cutoff = datetime.utcnow() - timedelta(days=30)
        unread_cutoff = datetime.utcnow() - timedelta(days=60)
        
        deleted_read = Message.query.filter(
            Message.is_read == True,
            Message.created_at < read_cutoff
        ).delete(synchronize_session=False)
        
        deleted_unread = Message.query.filter(
            Message.is_read == False,
            Message.created_at < unread_cutoff
        ).delete(synchronize_session=False)
        
        db.session.commit()
        logger.info(f"消息清理完成：已读{deleted_read}条，未读{deleted_unread}条")
    except Exception as e:
        logger.error(f"消息清理失败: {e}")
