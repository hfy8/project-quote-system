-- Migration 017: module_materials 表加 material_type 字段 (快照物料类型)
-- 业务含义: 报价单添加物料时, 把 material 的类型 (机械类/非机械类) 快照到 module_materials 表.
-- 跟 operation_log 的 employee_no + cn_name 快照思路一致, 历史报价单不受 Material.type 后续修改影响.
-- 取值: 'mechanical' (机械类) / 'electrical' (非机械类-电控) / 'other' (其他)
-- 默认值: 'other' (兼容旧数据, 老 module_materials 行没有 type 概念)

ALTER TABLE module_materials
    ADD COLUMN IF NOT EXISTS material_type VARCHAR(20) NOT NULL DEFAULT 'other';

-- 索引: 按类型筛选报价单物料
CREATE INDEX IF NOT EXISTS ix_module_materials_material_type ON module_materials(material_type);

COMMENT ON COLUMN module_materials.material_type IS '快照物料类型: mechanical=机械类, electrical=非机械类(电控), other=其他';

-- 回填: 从 materials 表读 type 写入 (确保历史数据也有 type)
UPDATE module_materials mm
SET material_type = m.material_type
FROM materials m
WHERE mm.material_id = m.id
  AND (mm.material_type = 'other' OR mm.material_type IS NULL)
  AND m.material_type IS NOT NULL;

-- 注意: 上面回填 UPDATE 可能让所有 'other' 的 mm 都用 m.material_type 覆盖, 这是符合用户意图的
-- (老 mm 没 type 概念, 现在统一从物料表读一遍, 后续添加会快照)