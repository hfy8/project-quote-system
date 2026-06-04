-- V2.1__material_key_params.sql
-- 添加原材料关键参数字段（灵活字段，供机构/电控选料参考）

ALTER TABLE materials ADD COLUMN IF NOT EXISTS param1 VARCHAR(100);
ALTER TABLE materials ADD COLUMN IF NOT EXISTS param2 VARCHAR(100);
ALTER TABLE materials ADD COLUMN IF NOT EXISTS param3 VARCHAR(100);