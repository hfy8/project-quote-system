-- Migration 018: materials 表加 product_name 字段 (产品名称)
-- 业务含义: 物料所属产品名称 (如"四轴机械手"、"点激光检测"), 用于模板优选清单"产品名称"列
-- 与 name (品名) 是两个独立维度:
--   - product_name: 产品名称 (产品线/分类) — 跨多个具体物料
--   - name:        品名 (具体型号名称) — 单个物料
-- 例: 物料"四轴机械手 ESPON LS6-B602S" — product_name="四轴机械手", name="四轴机械手"
--     物料"高精度2D激光位移传感器感测头 KEYENCE LJ-G015" — product_name="点激光检测", name="高精度2D激光位移传感器感测头"
-- 取值: VARCHAR(100), 允许为空 (老物料没这个概念)
-- 创建时间: 2026-07-15

ALTER TABLE materials
    ADD COLUMN IF NOT EXISTS product_name VARCHAR(100) NULL;

CREATE INDEX IF NOT EXISTS ix_materials_product_name ON materials(product_name) WHERE product_name IS NOT NULL;

COMMENT ON COLUMN materials.product_name IS '产品名称: 用于优选清单模板, 与品名(name)是产品线/具体型号两层维度';