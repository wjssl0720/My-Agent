from fastapi import APIRouter, Depends
from api.deps import get_caller_context
from context.caller_context import CallerContext
from core.models import CreateSessionRequest, CreateSessionResponse, SendMessageRequest, SendMessageResponse
from runtime.orchestrator import AgentOrchestrator
from sessions.store import SessionStore

router = APIRouter(tags=["sessions"])
session_store = SessionStore.default()

@router.post("/sessions", response_model=CreateSessionResponse)
async def create_session(
    req: CreateSessionRequest,
    caller: CallerContext = Depends(get_caller_context),
) -> CreateSessionResponse:
    session = session_store.create(caller=caller, agent_id=req.agent_id, metadata=req.metadata)
    return CreateSessionResponse(session_id=session.session_id, agent_id=session.agent_id)

@router.post("/sessions/{session_id}/messages", response_model=SendMessageResponse)
async def send_message(
    session_id: str,
    req: SendMessageRequest,
    caller: CallerContext = Depends(get_caller_context),
) -> SendMessageResponse:
    orchestrator = AgentOrchestrator.default_for_api()
    return await orchestrator.invoke(session_id=session_id, req=req, caller=caller)
