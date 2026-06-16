"""AI 工具阶段 5-A/5-B/5-C 单元测试 + 阶段 6 权限测试

覆盖 33 个工具中需要 DB 连接的部分（共 18 个需要 DB）：
- 读工具：返回 JSON 可解析 + 含预期字段
- 写工具：权限校验 + 日志记录

不需要 DB 的工具（纯计算类如 calculate_quotation_cost）不在此测试范围内。
"""
import json
import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DEEPSEEK_API_KEY", "dummy")

from core.services.ai_tools import TOOLS, TOOL_FUNCTIONS, execute_tool
from core.services.ai_guard import get_required_permission


# ============== Fixture：共享 session ==============

@pytest.fixture(scope="module")
def admin_user_id():
    """获取 admin 用户 ID"""
    from core.models.user import User
    from db import db_session_factory
    s = db_session_factory()
    try:
        u = s.query(User).filter(User.role == "admin").first()
        return u.id if u else 2
    finally:
        s.close()


@pytest.fixture(scope="module")
def viewer_user_id():
    """获取非 admin 用户（用于测试权限拒绝）"""
    from core.models.user import User
    from db import db_session_factory
    s = db_session_factory()
    try:
        u = s.query(User).filter(User.role != "admin").first()
        return u.id if u else 34
    finally:
        s.close()


@pytest.fixture(scope="module")
def business_user_id():
    """获取业务员用户（有 quotation.edit 权限）"""
    from core.models.user import User
    from db import db_session_factory
    s = db_session_factory()
    try:
        u = s.query(User).filter(User.role == "business").first()
        return u.id if u else None
    finally:
        s.close()


# ============== 基础校验：所有工具注册 ==============

class TestRegistration:
    def test_tool_count(self):
        """33 个工具"""
        assert len(TOOLS) == 33, f"期望 33 个工具，实际 {len(TOOLS)}"

    def test_tools_and_functions_match(self):
        """TOOLS 和 TOOL_FUNCTIONS 完全对应"""
        tool_names = {t["function"]["name"] for t in TOOLS}
        func_names = set(TOOL_FUNCTIONS.keys())
        assert tool_names == func_names, f"差异: TOOLS-FUNCS={tool_names-func_names}, FUNCS-TOOLS={func_names-tool_names}"

    def test_every_tool_has_description(self):
        """每个工具必须有 description"""
        for t in TOOLS:
            assert t["function"].get("description"), f"工具 {t['function']['name']} 缺少描述"


# ============== 只读工具 ==============

class TestReadTools:
    def test_list_quotations_v2(self):
        r = json.loads(execute_tool("list_quotations_v2", {"limit": 5}))
        assert "quotations" in r
        assert "total" in r
        assert r["total"] <= 5

    def test_list_quotations_v2_filter(self):
        r = json.loads(execute_tool("list_quotations_v2", {"status": "approved", "limit": 10}))
        for q in r.get("quotations", []):
            assert q["status"] == "approved"

    def test_get_quotation_full_existing(self):
        r = json.loads(execute_tool("get_quotation_full", {"quotation_id": 14}))
        assert r["id"] == 14
        assert "modules" in r
        assert "other_fees" in r
        assert "labor_hours" in r

    def test_get_quotation_full_not_found(self):
        r = json.loads(execute_tool("get_quotation_full", {"quotation_id": 99999}))
        assert "error" in r

    def test_search_materials_v2(self):
        r = json.loads(execute_tool("search_materials_v2", {"limit": 5}))
        assert "materials" in r

    def test_search_materials_v2_filter(self):
        r = json.loads(execute_tool("search_materials_v2", {"category": "standard", "limit": 10}))
        for m in r.get("materials", []):
            assert m["category"] == "standard"

    def test_list_material_categories(self):
        r = json.loads(execute_tool("list_material_categories", {}))
        assert "categories" in r
        assert len(r["categories"]) >= 1

    def test_get_quotation_travel_cost(self):
        r = json.loads(execute_tool("get_quotation_travel_cost", {"quotation_id": 14}))
        assert r["quotation_id"] == 14
        assert "grand_total" in r

    def test_get_quotation_fees(self):
        r = json.loads(execute_tool("get_quotation_fees", {"quotation_id": 14}))
        assert r["quotation_id"] == 14
        assert "by_type" in r

    def test_list_org_structure(self):
        r = json.loads(execute_tool("list_org_structure", {}))
        assert "departments" in r
        assert r["total_depts"] >= 1

    def test_who_can_approve(self):
        r = json.loads(execute_tool("who_can_approve", {"action": "approve"}))
        assert "matches" in r or "message" in r

    def test_find_user(self):
        r = json.loads(execute_tool("find_user", {"keyword": "admin"}))
        assert "users" in r
        assert r["total"] >= 1

    def test_find_user_not_found(self):
        r = json.loads(execute_tool("find_user", {"keyword": "不存在的人_xyz"}))
        assert "users" not in r or r.get("total", 0) == 0

    def test_list_pending_tasks(self):
        r = json.loads(execute_tool("list_pending_tasks", {}))
        assert "pending_quotations" in r

    def test_list_knowledge(self):
        r = json.loads(execute_tool("list_knowledge", {"limit": 5}))
        assert "documents" in r

    def test_list_my_conversations(self):
        r = json.loads(execute_tool("list_my_conversations", {"limit": 5}))
        assert "conversations" in r
        assert "note" in r  # 提示内存存储

    def test_get_knowledge_stats(self):
        r = json.loads(execute_tool("get_knowledge_stats", {}))
        assert "total" in r

    def test_export_quotation_excel(self):
        r = json.loads(execute_tool("export_quotation", {"quotation_id": 14, "format": "excel"}))
        assert r["format"] == "excel"
        assert "download_url" in r

    def test_export_quotation_invalid_format(self):
        r = json.loads(execute_tool("export_quotation", {"quotation_id": 14, "format": "xml"}))
        assert "error" in r


# ============== 阶段 6：写工具 + 权限校验 ==============

class TestWriteToolsPermission:
    def test_no_user_id_for_write(self):
        """写工具不传 user_id → 拒绝"""
        r = json.loads(execute_tool("delete_knowledge", {"doc_id": 999}))
        assert "error" in r
        assert "user_id" in r["error"]

    def test_viewer_cannot_delete_knowledge(self, viewer_user_id):
        """viewer 角色无 system.edit → 拒绝"""
        r = json.loads(execute_tool("delete_knowledge", {"doc_id": 999}, user_id=viewer_user_id))
        assert "error" in r
        assert "权限不足" in r["error"]

    def test_admin_can_delete_knowledge_not_found(self, admin_user_id):
        """admin 删除不存在的 doc → 业务错误（权限通过）"""
        r = json.loads(execute_tool("delete_knowledge", {"doc_id": 99999}, user_id=admin_user_id))
        assert "error" in r
        # 业务错误，不是权限错误
        assert "权限" not in r["error"]

    def test_business_can_update_quotation_status(self, business_user_id):
        """business 用户能改状态（有 quotation.edit）"""
        if not business_user_id:
            pytest.skip("no business user")
        # 选一个 draft 状态的报价单测试
        from core.models.quotation import Quotation
        from db import db_session_factory
        s = db_session_factory()
        try:
            draft_q = s.query(Quotation).filter(Quotation.status == "draft").first()
            if not draft_q:
                pytest.skip("no draft quotation to test")
            qid = draft_q.id
        finally:
            s.close()

        # 切换到 approved
        r = json.loads(execute_tool(
            "update_quotation_status",
            {"quotation_id": qid, "new_status": "approved"},
            user_id=business_user_id
        ))
        assert r.get("success") is True or "已批准" in r.get("message", "")

        # 切回 draft（清理）
        r2 = json.loads(execute_tool(
            "update_quotation_status",
            {"quotation_id": qid, "new_status": "draft"},
            user_id=business_user_id
        ))
        assert r2.get("success") is True or "草稿" in r2.get("message", "")

    def test_business_cannot_delete_knowledge(self, business_user_id):
        """business 用户没 system.edit → 拒绝"""
        if not business_user_id:
            pytest.skip("no business user")
        r = json.loads(execute_tool(
            "delete_knowledge",
            {"doc_id": 999},
            user_id=business_user_id
        ))
        assert "error" in r
        assert "权限不足" in r["error"]


# ============== 日志验证 ==============

class TestOperationLog:
    def test_write_action_creates_log(self, admin_user_id):
        """写工具调用后应写入 OperationLog"""
        from core.models.operation_log import OperationLog
        from db import db_session_factory
        from sqlalchemy import desc

        # 调用写工具
        execute_tool("delete_knowledge", {"doc_id": 99999}, user_id=admin_user_id)

        # 查最新日志
        s = db_session_factory()
        try:
            latest = s.query(OperationLog).filter(
                OperationLog.detail.like("[AI:delete_knowledge]%")
            ).order_by(desc(OperationLog.id)).first()
            assert latest is not None
            assert latest.username == "admin"
            assert "[AI:delete_knowledge]" in latest.detail
        finally:
            s.close()

    def test_permission_denied_creates_log(self, viewer_user_id):
        """权限拒绝也应记录日志"""
        from core.models.operation_log import OperationLog
        from db import db_session_factory
        from sqlalchemy import desc

        execute_tool("delete_knowledge", {"doc_id": 999}, user_id=viewer_user_id)

        s = db_session_factory()
        try:
            # viewer 实际用户名可能是其他（fixture 拿到的是非 admin 第一个）
            from core.models.user import User
            viewer_user = s.query(User).get(viewer_user_id)
            viewer_name = viewer_user.username if viewer_user else None

            if not viewer_name:
                pytest.skip("viewer_name not found")

            recent_log = s.query(OperationLog).filter(
                OperationLog.detail.like("[AI:delete_knowledge]%"),
                OperationLog.username == viewer_name,
            ).order_by(desc(OperationLog.id)).first()
            assert recent_log is not None
            assert "缺少权限" in recent_log.detail
            assert "success=False" in recent_log.detail
        finally:
            s.close()

    def test_read_tool_no_log(self, admin_user_id):
        """只读工具不应写日志"""
        from core.models.operation_log import OperationLog
        from db import db_session_factory
        from sqlalchemy import desc

        # 记录调用前的最新日志 id
        s = db_session_factory()
        try:
            before_max = s.query(OperationLog).order_by(desc(OperationLog.id)).first()
            before_id = before_max.id if before_max else 0
        finally:
            s.close()

        # 调只读工具
        execute_tool("list_quotations_v2", {"limit": 3})

        # 不应有新日志
        s = db_session_factory()
        try:
            after_max = s.query(OperationLog).order_by(desc(OperationLog.id)).first()
            after_id = after_max.id if after_max else 0
            # 因为其他测试可能写日志，不能严格断言 ==，但不应有 [AI:list_quotations_v2]
            read_log = s.query(OperationLog).filter(
                OperationLog.detail.like("[AI:list_quotations_v2]%")
            ).first()
            assert read_log is None
        finally:
            s.close()


# ============== 边界 case ==============

class TestEdgeCases:
    def test_unknown_tool(self):
        r = json.loads(execute_tool("nonexistent_tool", {}))
        assert "error" in r

    def test_empty_search_materials(self):
        r = json.loads(execute_tool("search_materials_v2", {"keyword": "不存在的xyz123"}))
        assert r.get("total", 0) == 0 or "materials" in r

    def test_zero_price_range(self):
        """0 表示不限，应该返回所有"""
        r = json.loads(execute_tool("search_materials_v2", {"min_price": 0, "max_price": 0, "limit": 5}))
        assert "materials" in r

    def test_invalid_quotation_id(self):
        r = json.loads(execute_tool("get_quotation_full", {"quotation_id": 0}))
        assert "error" in r