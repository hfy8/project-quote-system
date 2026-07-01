-- ============================================
-- Migration 013 (FIXED): 给所有无品号物料批量生成 item_no
-- ============================================
-- 规则: MAT-{CATEGORY}-{6位编号}-{BRAND代码}
--   - 前缀: MAT-
--   - 类别: LAR (大件) / STD (核心部件)
--   - 编号: 6 位零填充, 按 id 顺序 (000001-999999)
--   - 品牌: 空/国产/纯中文 → GCN, 国际品牌按规则取首字母
--   - 示例: MAT-LAR-000001-GCN / MAT-LAR-000008-HIW / MAT-LAR-000012-THK
-- ============================================
-- 幂等: 排除"其他"物料 (id=184, 品号=其他)
-- 修复: 重置所有刚生成的 MAT-* 品号为 NULL, 再重新生成 (避免 id=38 等被错误覆盖)

BEGIN;

-- 0. 把所有 MAT- 开头的品号重置为 NULL (上轮重复生成的), 排除"其他"
UPDATE materials
SET item_no = NULL
WHERE item_no LIKE 'MAT-%'
  AND id != 184;

-- 1. 用 CTE + row_number() 按 (category, id) 顺序生成编号
WITH numbered AS (
    SELECT
        id,
        CASE
            -- 空品牌 / 国产 / 中文品牌 → GCN (GuoChan National)
            WHEN brand IS NULL OR brand = '' OR brand = '国产' THEN 'GCN'
            WHEN brand !~ '[A-Za-z]' THEN 'GCN'  -- 纯中文品牌
            -- 国际品牌首字母规则
            WHEN UPPER(brand) LIKE 'HIWIN%' OR brand LIKE '%上银%' THEN 'HIW'
            WHEN UPPER(brand) LIKE 'SIEMENS%' OR brand LIKE '%西门子%' THEN 'SIE'
            WHEN UPPER(brand) LIKE 'SCHNEIDER%' OR brand LIKE '%施耐德%' THEN 'SCH'
            WHEN UPPER(brand) LIKE 'PILZ%' OR brand LIKE '%皮尔兹%' THEN 'PIL'
            WHEN UPPER(brand) LIKE 'THK%' THEN 'THK'
            WHEN UPPER(brand) LIKE 'MISUMI%' OR brand LIKE '%米思米%' THEN 'MIS'
            WHEN UPPER(brand) LIKE 'FESTO%' OR brand LIKE '%费斯托%' THEN 'FES'
            WHEN UPPER(brand) LIKE 'SMC%' THEN 'SMC'
            WHEN UPPER(brand) LIKE 'OMRON%' OR brand LIKE '%欧姆龙%' THEN 'OMR'
            -- 未知英文品牌: 取首 3 个 ASCII 字符
            ELSE UPPER(LEFT(REGEXP_REPLACE(brand, '[^A-Za-z]', '', 'g'), 3))
        END AS brand_code,
        CASE category
            WHEN 'large' THEN 'LAR'
            WHEN 'standard' THEN 'STD'
            ELSE 'OTH'
        END AS category_code,
        ROW_NUMBER() OVER (
            PARTITION BY category
            ORDER BY id
        ) AS rn
    FROM materials
    WHERE id != 184  -- 排除"其他"
      AND (item_no IS NULL OR item_no = '' OR item_no = '其他')
)

-- 更新 item_no (从 NULL 开始填充, 不会覆盖已有合规品号)
UPDATE materials m
SET item_no = 'MAT-' || n.category_code || '-' || LPAD(n.rn::text, 6, '0') || '-' || n.brand_code
FROM numbered n
WHERE m.id = n.id;

COMMIT;

-- 验证
SELECT
    category,
    COUNT(*) AS total,
    COUNT(*) FILTER (WHERE item_no IS NOT NULL AND item_no != '') AS with_item_no,
    COUNT(*) FILTER (WHERE item_no IS NULL OR item_no = '') AS without_item_no
FROM materials
GROUP BY category
ORDER BY category;

-- 检查是否还有以 "-" 结尾的不合规品号
SELECT COUNT(*) AS bad_item_no_count FROM materials WHERE item_no ~ '-$';

-- 唯一性 (必须 0 行)
SELECT item_no, COUNT(*) AS dup_count
FROM materials
WHERE item_no IS NOT NULL AND item_no != ''
GROUP BY item_no
HAVING COUNT(*) > 1;

-- 大件样本 (看品牌处理)
SELECT id, name, brand, item_no
FROM materials
WHERE category = 'large'
ORDER BY id
LIMIT 20;

-- 核心部件样本
SELECT id, name, brand, item_no
FROM materials
WHERE category = 'standard'
ORDER BY id
LIMIT 20;

-- "其他"物料 id=184 验证
SELECT id, name, item_no FROM materials WHERE id = 184;

-- 品牌代码分布
SELECT
    REGEXP_MATCHES(item_no, '-(GCN|HIW|SIE|SCH|PIL|THK|MIS|FES|SMC|OMR|[A-Z]{3})$') AS brand_code,
    COUNT(*) AS count
FROM materials
WHERE item_no LIKE 'MAT-%'
GROUP BY brand_code
ORDER BY count DESC;