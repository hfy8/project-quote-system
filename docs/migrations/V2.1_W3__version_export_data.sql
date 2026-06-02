-- V2.1 W3: 版本管理域 - export_data 字段
-- Author: hermes
-- Date: 2026-06-02

ALTER TABLE version_snapshots ADD COLUMN export_data TEXT;

COMMENT ON COLUMN version_snapshots.export_data IS '脱敏导出数据JSON，用于高效渲染/导出';