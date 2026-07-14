-- V2.1.5: 操作日志增加工号和中文姓名字段（快照）
-- 写日志时把 user 当前对应的 employee_no / cn_name 写入历史记录
-- 防止以后员工改名/转岗/离职后，历史日志无法辨识操作者

ALTER TABLE operation_logs ADD COLUMN IF NOT EXISTS employee_no VARCHAR(50);
ALTER TABLE operation_logs ADD COLUMN IF NOT EXISTS cn_name VARCHAR(100);
CREATE INDEX IF NOT EXISTS ix_operation_logs_employee_no ON operation_logs(employee_no);

-- 回填: 从 users + employees 把历史日志的工号和姓名补上
-- 用 LEFT JOIN 兼容 user_id 找不到/employee 关联缺失的情况
UPDATE operation_logs ol
SET
    employee_no = e.employee_no,
    cn_name     = e.cn_name
FROM users u
LEFT JOIN employees e ON e.id = u.employee_id
WHERE u.id = ol.user_id
  AND ol.employee_no IS NULL
  AND ol.cn_name IS NULL;

-- 验证
SELECT COUNT(*) AS total,
       COUNT(employee_no) AS has_employee_no,
       COUNT(cn_name) AS has_cn_name
FROM operation_logs;