-- V2.1 新增表：运输与差旅费用（系统配置层 + 项目层）
-- 运行前请备份数据库

BEGIN;

-- ===== 系统配置层 =====

-- 1. 包装类型
CREATE TABLE IF NOT EXISTS packing_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    name_en VARCHAR(100),
    unit_price DECIMAL(12,2) NOT NULL DEFAULT 0,
    description TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. 差旅分类
CREATE TABLE IF NOT EXISTS travel_categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    name_en VARCHAR(100),
    code VARCHAR(50) NOT NULL UNIQUE,
    sort_order INTEGER NOT NULL DEFAULT 0,
    description TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. 差旅人天单价（分类 × 单价）
CREATE TABLE IF NOT EXISTS travel_day_rates (
    id SERIAL PRIMARY KEY,
    travel_category_id INTEGER NOT NULL REFERENCES travel_categories(id) ON DELETE CASCADE,
    unit_price DECIMAL(12,2) NOT NULL DEFAULT 0,
    currency VARCHAR(10) NOT NULL DEFAULT 'CNY',
    description TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(travel_category_id)
);

-- 4. 出行方式
CREATE TABLE IF NOT EXISTS travel_modes (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    name_en VARCHAR(100),
    code VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. 差旅人次单价矩阵（分类 × 出行方式 × 单价）
CREATE TABLE IF NOT EXISTS travel_person_trip_fees (
    id SERIAL PRIMARY KEY,
    travel_category_id INTEGER NOT NULL REFERENCES travel_categories(id) ON DELETE CASCADE,
    travel_mode_id INTEGER NOT NULL REFERENCES travel_modes(id) ON DELETE CASCADE,
    unit_price DECIMAL(12,2) NOT NULL DEFAULT 0,
    visa_fee DECIMAL(12,2) NOT NULL DEFAULT 0,
    currency VARCHAR(10) NOT NULL DEFAULT 'CNY',
    description TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(travel_category_id, travel_mode_id)
);

-- ===== 项目层 =====

-- 6. 包装条目（项目层录入：按 quotation_id + packing_type_id 唯一）
CREATE TABLE IF NOT EXISTS packing_entries (
    id SERIAL PRIMARY KEY,
    quotation_id INTEGER NOT NULL REFERENCES quotations(id) ON DELETE CASCADE,
    packing_type_id INTEGER NOT NULL REFERENCES packing_types(id) ON DELETE CASCADE,
    quantity DECIMAL(12,2) NOT NULL DEFAULT 0,
    remark TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(quotation_id, packing_type_id)
);

-- 7. 差旅人天条目（项目层录入：按 quotation_id + travel_category_id 唯一）
CREATE TABLE IF NOT EXISTS travel_person_days (
    id SERIAL PRIMARY KEY,
    quotation_id INTEGER NOT NULL REFERENCES quotations(id) ON DELETE CASCADE,
    travel_category_id INTEGER NOT NULL REFERENCES travel_categories(id) ON DELETE CASCADE,
    person_days DECIMAL(12,2) NOT NULL DEFAULT 0,
    remark TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(quotation_id, travel_category_id)
);

-- 8. 差旅人次条目（项目层录入：按 quotation_id + travel_category_id + travel_mode_id 唯一）
CREATE TABLE IF NOT EXISTS travel_person_trips (
    id SERIAL PRIMARY KEY,
    quotation_id INTEGER NOT NULL REFERENCES quotations(id) ON DELETE CASCADE,
    travel_category_id INTEGER NOT NULL REFERENCES travel_categories(id) ON DELETE CASCADE,
    travel_mode_id INTEGER NOT NULL REFERENCES travel_modes(id) ON DELETE CASCADE,
    person_count INTEGER NOT NULL DEFAULT 0,
    remark TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(quotation_id, travel_category_id, travel_mode_id)
);

COMMIT;
