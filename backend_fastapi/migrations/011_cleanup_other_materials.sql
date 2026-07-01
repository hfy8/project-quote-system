-- ============================================
-- Migration 011: 清理"其他"类原材料
-- ============================================
-- 目的:
--   1) 删除所有 category='other' 的物料 (39 个)
--   2) 删除这些物料在 module_materials 的引用 (15 条)
--   3) 插入 1 个标准"其他"物料
-- ============================================

BEGIN;

-- 1. 先删引用 (否则 materials 删不掉, FK 报错)
DELETE FROM module_materials
WHERE material_id IN (
    SELECT id FROM materials WHERE category = 'other'
);

-- 2. 删所有"其他"类物料
DELETE FROM materials WHERE category = 'other';

-- 3. 同步 SERIAL 序列 (max+1, is_called=true, 下次 nextval = max+1)
SELECT setval(pg_get_serial_sequence('materials', 'id'),
              COALESCE((SELECT MAX(id) FROM materials), 0),
              true);

-- 4. 插入 1 个标准"其他"物料
INSERT INTO materials (
    name, spec, unit, unit_price, category,
    item_no, param1, param2, param3, status,
    created_at
) VALUES (
    '其他',
    '其他',
    'SET',
    0,
    'other',
    '其他',
    '其他',
    '其他',
    '其他',
    'active',
    NOW()
);

COMMIT;

-- 验证
SELECT id, name, spec, unit, unit_price, category, item_no, param1, param2, param3, status
FROM materials WHERE category = 'other';
SELECT COUNT(*) AS other_total FROM materials WHERE category = 'other';
SELECT COUNT(*) AS other_module_materials FROM module_materials mm
JOIN materials m ON m.id = mm.material_id
WHERE m.category = 'other';