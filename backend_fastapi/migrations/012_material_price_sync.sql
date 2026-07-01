-- ============================================
-- Migration 012: 原材料价格同步跟踪字段
-- ============================================
-- 目的:
--   - 记录每个物料最近一次价格同步的状态 (时间 / 是否成功 / 来源)
--   - 加 partial index, 方便查询"有品号"的待同步物料
-- ============================================

ALTER TABLE materials
    ADD COLUMN IF NOT EXISTS last_price_synced_at TIMESTAMP,
    ADD COLUMN IF NOT EXISTS last_price_sync_status VARCHAR(20),
        -- 'success' / 'failed' / 'skipped' / 'pending'
    ADD COLUMN IF NOT EXISTS last_price_sync_error TEXT,
    ADD COLUMN IF NOT EXISTS last_price_sync_source VARCHAR(100);
        -- 来源 (e.g. 'mock-api' / 'erp.example.com')

-- 部分索引: 只索引有品号的物料 (这些才是同步候选)
-- 注意: idx_materials_item_no 已经存在 (WHERE NOT NULL), 复用即可

-- 验证
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'materials'
  AND column_name LIKE 'last_price%'
ORDER BY column_name;