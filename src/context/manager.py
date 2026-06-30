from context.caller_context import CallerContext
from context.context_pack import ContextPack
from permissions.permission_engine import PermissionEngine

class ContextManager:
    def __init__(self, permission_engine: PermissionEngine | None = None) -> None:
        self.permission_engine = permission_engine or PermissionEngine.default()

    def build(
        self,
        *,
        caller: CallerContext,
        session_id: str,
        agent_id: str,
        file_ids: list[str],
        short_term_memory: dict,
    ) -> ContextPack:
        return ContextPack(
            caller=caller,
            session_id=session_id,
            agent_id=agent_id,
            file_ids=file_ids,
            short_term_memory=short_term_memory,
            allowed_rag_scopes=self.permission_engine.allowed_rag_scopes(caller),
        )
