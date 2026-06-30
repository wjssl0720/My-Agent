from fastapi import Header
from context.caller_context import CallerContext

async def get_caller_context(
    x_user_id: str = Header(default="anonymous"),
    x_department: str = Header(default="guest"),
    x_roles: str = Header(default=""),
    x_tenant_id: str = Header(default="default"),
    x_request_id: str | None = Header(default=None),
) -> CallerContext:
    roles = [r.strip() for r in x_roles.split(",") if r.strip()] or ["guest"]
    return CallerContext(
        user_id=x_user_id,
        tenant_id=x_tenant_id,
        department=x_department,
        roles=roles,
        request_id=x_request_id,
    )
