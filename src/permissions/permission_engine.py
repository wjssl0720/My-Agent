from context.caller_context import CallerContext
from permissions.models import PermissionDecision

class PermissionEngine:
    def __init__(self) -> None:
        self.role_rules = {
            "guest": {"allow_tools": ["rag.search"], "deny_tools": [], "require_approval": []},
            "operator": {
                "allow_tools": ["rag.search", "product.get_sku", "product.search_similar"],
                "deny_tools": ["bi.run_readonly_sql", "order.refund"],
                "require_approval": [],
            },
            "analyst": {
                "allow_tools": [
                    "rag.search", "product.get_sku", "product.search_similar",
                    "bi.run_readonly_sql", "bi.generate_report",
                ],
                "deny_tools": [],
                "require_approval": [],
            },
            "customer_service": {
                "allow_tools": ["rag.search", "product.get_sku", "order.get_order"],
                "deny_tools": [],
                "require_approval": ["order.refund"],
            },
        }
        self.rag_scope_rules = {
            "ecommerce": ["product_docs", "operation_docs"],
            "cs": ["customer_service_docs", "product_docs"],
            "finance": ["finance_docs"],
            "guest": [],
        }

    @classmethod
    def default(cls) -> "PermissionEngine":
        return cls()

    def decide_tool(self, caller: CallerContext, tool_name: str, args: dict) -> PermissionDecision:
        allow: set[str] = set()
        deny: set[str] = set()
        ask: set[str] = set()

        for role in caller.roles:
            rule = self.role_rules.get(role, {})
            allow.update(rule.get("allow_tools", []))
            deny.update(rule.get("deny_tools", []))
            ask.update(rule.get("require_approval", []))

        if tool_name in deny:
            return PermissionDecision("deny", f"role denies tool {tool_name}")
        if tool_name in ask:
            return PermissionDecision("ask", f"tool {tool_name} requires human approval")
        if tool_name in allow:
            return PermissionDecision("allow", f"role allows tool {tool_name}")
        return PermissionDecision("deny", f"tool {tool_name} is not allowed for roles={caller.roles}")

    def allowed_rag_scopes(self, caller: CallerContext) -> list[str]:
        return self.rag_scope_rules.get(caller.department, [])
