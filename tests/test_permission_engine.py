from context.caller_context import CallerContext
from permissions.permission_engine import PermissionEngine

def test_operator_denied_bi_sql():
    engine = PermissionEngine.default()
    caller = CallerContext(user_id="u1", department="ecommerce", roles=["operator"])
    decision = engine.decide_tool(caller, "bi.run_readonly_sql", {})
    assert decision.decision == "deny"

def test_customer_service_refund_requires_approval():
    engine = PermissionEngine.default()
    caller = CallerContext(user_id="u1", department="cs", roles=["customer_service"])
    decision = engine.decide_tool(caller, "order.refund", {})
    assert decision.decision == "ask"
