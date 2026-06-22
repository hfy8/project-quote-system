-- ============================================
-- PostgreSQL 初始化脚本 (v17 Docker 部署)
-- 自动执行: docker-entrypoint-initdb.d/
-- 用途: 创建 quotation_db 扩展 + 基础配置
-- ============================================

-- 启用 pgvector 扩展（AI 工具 RAG 检索需要）
CREATE EXTENSION IF NOT EXISTS vector;

-- 启用常用扩展
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- 中文全文搜索
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- 输出确认
DO $$
BEGIN
    RAISE NOTICE '✅ pgvector 已启用，DB 初始化完成';
    RAISE NOTICE '   向量维度: 1536 (OpenAI 兼容) / 1024 (智源)';
END $$;
