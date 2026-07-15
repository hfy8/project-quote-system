-- Migration 019: module_materials 快照 product_name + category
-- 业务背景: 用户要求报价单添加物料时记录产品名称 + 部件分类, 后续物料表改了不影响历史
-- 跟 migration 017 (material_type 快照) 思路一致

ALTER TABLE module_materials
    ADD COLUMN IF NOT EXISTS product_name VARCHAR(100) NULL,
    ADD COLUMN IF NOT EXISTS category VARCHAR(20) NULL;

-- 部分索引
CREATE INDEX IF NOT EXISTS ix_module_materials_product_name ON module_materials(product_name) WHERE product_name IS NOT NULL;
CREATE INDEX IF NOT EXISTS ix_module_materials_category ON module_materials(category) WHERE category IS NOT NULL;

-- 回填历史数据
UPDATE module_materials mm SET
    product_name = m.product_name,
    category = m.category
FROM materials m
WHERE mm.material_id = m.id
  AND (mm.product_name IS NULL OR mm.category IS NULL);

COMMENT ON COLUMN module_materials.product_name IS '产品名称 (产品线) 快照 - 防止物料表 product_name 修改影响历史报价单';
COMMENT ON COLUMN module_materials.category IS '部件分类 快照 - 防止物料表 category 修改影响历史报价单';