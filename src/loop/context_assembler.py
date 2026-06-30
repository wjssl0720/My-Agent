from agents.profiles import AgentProfile
from context.context_pack import ContextPack

class ContextAssembler:
    def assemble(self, profile: AgentProfile, context: ContextPack, message: str) -> dict:
        return {
            "agent_id": profile.agent_id,
            "caller": context.caller.model_dump(),
            "session_id": context.session_id,
            "file_ids": context.file_ids,
            "memory": context.short_term_memory,
            "business_context": context.business_context,
            "user_message": message,
        }
