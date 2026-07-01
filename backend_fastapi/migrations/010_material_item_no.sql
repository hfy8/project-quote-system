-- 010_material_item_no.sql
-- 原材料加品号 (item_no) 字段, 跨系统同步用, 允许为空
ALTER TABLE materials ADD COLUMN IF NOT EXISTS item_no VARCHAR(50);
CREATE INDEX IF NOT EXISTS idx_materials_item_no ON materials(item_no) WHERE item_no IS NOT NULL;
