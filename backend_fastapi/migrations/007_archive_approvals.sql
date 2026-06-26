-- 报价单归档审批流
-- 新增 archive_approvals 表 + 扩展 quotation status 取值

-- 1. 加新表
CREATE TABLE IF NOT EXISTS archive_approvals (
    id              SERIAL PRIMARY KEY,
    quotation_id    INTEGER NOT NULL REFERENCES quotations(id) ON DELETE CASCADE,
    requested_by    INTEGER NOT NULL REFERENCES users(id),
    requested_at    TIMESTAMP NOT NULL DEFAULT NOW(),
    approver_id     INTEGER NOT NULL REFERENCES users(id),
    approved_at     TIMESTAMP,
    status          VARCHAR(20) NOT NULL DEFAULT 'pending',  -- pending/approved/rejected/cancelled
    reject_reason   TEXT,
    via             VARCHAR(20) NOT NULL DEFAULT 'approval', -- approval/admin (admin 直接归档留痕)
    remark          TEXT,
    metadata        JSONB
);

-- 索引: 部门领导查待办 (只查自己作为 approver + pending 的)
CREATE INDEX IF NOT EXISTS idx_archive_approvals_approver_pending
    ON archive_approvals(approver_id, status)
    WHERE status = 'pending';

-- 索引: 报价单维度 (一个报价单同一时间只有一个 pending)
CREATE INDEX IF NOT EXISTS idx_archive_approvals_quotation
    ON archive_approvals(quotation_id);

-- 索引: 发起人维度
CREATE INDEX IF NOT EXISTS idx_archive_approvals_requester
    ON archive_approvals(requested_by);

-- 2. 报价单 status 现在是 varchar(20), 无 CHECK, 自动支持新值 'approved_pending'
-- 现有 valid_transitions 需要扩展 (在 Python 代码里改, 不动 DB)

-- 3. 兼容: 没配置部门的用户尝试发起归档会报错 (已在前端 + 后端兜底)