-- Migration 016: materials 表加 material_type 字段
-- 业务含义: 物料所属类型 (机械类/非机械类), 与 category (大件/核心部件/其他件) 是两个独立维度
--   - category: 物料分类 (尺寸/地位)
--   - material_type: 物料所属类型 (机械类/非机械类) — 跟模板优选清单的"类型"列对应
-- 取值: 'mechanical' (机械类), 'electrical' (非机械类 - 电控类), 'other' (非机械类 - 其他)
-- 默认值: 'other' (兼容旧数据)
-- 创建时间: 2026-07-15

ALTER TABLE materials
    ADD COLUMN IF NOT EXISTS material_type VARCHAR(20) NOT NULL DEFAULT 'other';

CREATE INDEX IF NOT EXISTS ix_materials_material_type ON materials(material_type);

COMMENT ON COLUMN materials.material_type IS '物料类型: mechanical=机械类, electrical=非机械类(电控), other=其他';