from uuid import uuid4
from pydantic import BaseModel, Field
from context.caller_context import CallerContext

class Session(BaseModel):
    session_id: str
    agent_id: str
    caller_user_id: str
    metadata: dict = Field(default_factory=dict)

class SessionStore:
    def __init__(self) -> None:
        self._sessions: dict[str, Session] = {}

    @classmethod
    def default(cls) -> "SessionStore":
        return cls()

    def create(self, caller: CallerContext, agent_id: str, metadata: dict) -> Session:
        session = Session(
            session_id=str(uuid4()),
            agent_id=agent_id,
            caller_user_id=caller.user_id,
            metadata=metadata,
        )
        self._sessions[session.session_id] = session
        return session
