-- B4: 移除 module_materials.unit_price 字段
-- 背景: DB 有这个字段 (137 行全 None), ORM model 没这个字段 (不同步)
-- 所有代码用 mm.unit_price_override 或 mm.material.unit_price, 这个字段没引用, DROP 安全
BEGIN;
ALTER TABLE module_materials DROP COLUMN IF EXISTS unit_price;
COMMIT;

-- 验证
SELECT column_name FROM information_schema.columns
WHERE table_name = 'module_materials'
ORDER BY ordinal_position;