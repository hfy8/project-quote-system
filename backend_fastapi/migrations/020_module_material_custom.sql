-- Migration 020: 自制件支持
-- 场景: 模块添加物料时, 这个物料在原材料库没有, 是自制件
-- 需求: 手动填写品名/规格/单位/单价/类型/部件分类/产品名称/品牌/关键参数
-- 方案: module_materials 加 is_custom 标记 + custom_data JSONB 存灵活字段
--       复用现有 material_type/product_name/category 快照字段
-- 零污染 Materials 表 (自制件不进物料库)
-- 自制件不进"导出无品号物料" (前端过滤)
--
-- v1.4.64: 自制件模块物料

ALTER TABLE module_materials
    ADD COLUMN IF NOT EXISTS is_custom BOOLEAN NOT NULL DEFAULT FALSE;

ALTER TABLE module_materials
    ADD COLUMN IF NOT EXISTS custom_data JSONB;

-- 自制件过滤索引
CREATE INDEX IF NOT EXISTS idx_module_materials_is_custom
  ON module_materials(module_id, is_custom);

COMMENT ON COLUMN module_materials.is_custom IS '自制件标记: true=原材料库无此物料, 用户手动填写 (字段存 custom_data JSONB)';
COMMENT ON COLUMN module_materials.custom_data IS '自制件灵活字段 JSONB: {name, spec, unit, brand, unit_price, param1, param2, param3}';

-- 同时需要把 material_id 改成 nullable (自制件时为 None)
ALTER TABLE module_materials ALTER COLUMN material_id DROP NOT NULL;