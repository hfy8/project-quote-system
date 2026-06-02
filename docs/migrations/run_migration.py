import psycopg2
import sys

sql = open('/home/rs8568/project-quote-system/docs/migrations/V2.1__travel_fees.sql').read()

attempts = [
    {'host': 'localhost', 'user': 'postgres', 'password': 'postgres', 'dbname': 'quotation_db'},
    {'host': 'localhost', 'user': 'postgres', 'password': 'admin', 'dbname': 'quotation_db'},
    {'host': '10.60.100.2', 'user': 'postgres', 'password': 'postgres', 'dbname': 'quotation_db'},
    {'host': '10.60.100.2', 'user': 'postgres', 'password': 'rspro123', 'dbname': 'quotation_db'},
]

for a in attempts:
    try:
        conn = psycopg2.connect(**a)
        conn.autocommit = True
        conn.cursor().execute(sql)
        print(f"✅ 迁移成功！连接: {a['host']}")
        sys.exit(0)
    except Exception as e:
        print(f"❌ {a['host']}: {e}")
        continue

print("⚠️ 无法连接数据库，请在 PostgreSQL 环境中手动执行迁移SQL")