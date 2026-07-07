
-- B3: fee_types 表 + FK + 数据迁移
BEGIN;

-- 1. 建 fee_types 表 (字段对齐 model)
CREATE TABLE IF NOT EXISTS fee_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    name_en VARCHAR(100),
    location VARCHAR(20) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);
CREATE UNIQUE INDEX IF NOT EXISTS idx_fee_types_name_unique ON fee_types(name) WHERE is_active = TRUE;

-- 2. seed 数据 (现有 2 种 fee_type)
INSERT INTO fee_types (name, name_en, location, is_active) VALUES
    ('认证费', 'Certification Fee', 'external', TRUE),
    ('项目管理费', 'Project Management Fee', 'external', TRUE)
ON CONFLICT DO NOTHING;

-- 3. 加 other_fees.fee_type_id FK (nullable, 不破坏现有)
ALTER TABLE other_fees ADD COLUMN IF NOT EXISTS fee_type_id INTEGER;
DO $$ BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_other_fees_fee_type_id') THEN
        ALTER TABLE other_fees ADD CONSTRAINT fk_other_fees_fee_type_id
            FOREIGN KEY (fee_type_id) REFERENCES fee_types(id) ON DELETE RESTRICT;
    END IF;
END $$;

-- 4. 数据迁移: fee_type 字符串 -> fee_type_id
UPDATE other_fees of
SET fee_type_id = ft.id
FROM fee_types ft
WHERE of.fee_type = ft.name
  AND of.fee_type_id IS NULL;

-- 5. 验证迁移结果
SELECT
    COUNT(*) AS total_fees,
    COUNT(fee_type_id) AS migrated,
    COUNT(*) - COUNT(fee_type_id) AS unmigrated
FROM other_fees;

COMMIT;
