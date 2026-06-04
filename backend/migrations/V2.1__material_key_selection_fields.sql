-- V2.1__material_key_selection_fields.sql
-- 添加原材料关键选型信息字段

ALTER TABLE materials ADD COLUMN IF NOT EXISTS manufacturer VARCHAR(100);
ALTER TABLE materials ADD COLUMN IF NOT EXISTS part_number VARCHAR(100);
ALTER TABLE materials ADD COLUMN IF NOT EXISTS lead_time VARCHAR(50);