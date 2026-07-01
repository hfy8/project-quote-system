-- 009_labor_type.sql
-- 人力工时加 labor_type 字段 (设计/调试/装配)
ALTER TABLE labor_hours ADD COLUMN IF NOT EXISTS labor_type VARCHAR(20) DEFAULT 'design';
ALTER TABLE labor_hours ADD CONSTRAINT IF NOT EXISTS ck_labor_hours_labor_type
    CHECK (labor_type IN ('design', 'debug', 'assembly'));
CREATE INDEX IF NOT EXISTS ix_labor_hours_labor_type ON labor_hours(labor_type);

-- 回填: 历史数据全部 default 'design' (没有具体语义)
UPDATE labor_hours SET labor_type = 'design' WHERE labor_type IS NULL;
