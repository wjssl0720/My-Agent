import pytest
from context.caller_context import CallerContext
from evaluation.dataset import EvaluationCase, EvaluationDataset
from evaluation.regression import RegressionRunner
from evaluation.report import EvaluationReport
from events.event_bus import EventBus
from events.event_schema import AgentEvent
from events.event_store import EventStore
from execution.task_runner import TaskRunner
from hooks.hook_event import HookContext, HookPoint, HookResult
from hooks.hook_registry import HookRegistry
from hooks.hook_runner import HookRunner
from workspace.artifact_store import ArtifactStore
from workspace.filesystem import WorkspaceFileSystem
from workspace.workspace_manager import WorkspaceManager

@pytest.mark.asyncio
async def test_workspace_artifact_roundtrip():
    caller = CallerContext(user_id="u1", tenant_id="t1", department="ecommerce", roles=["operator"])
    workspace = await WorkspaceManager.default().create(caller=caller, session_id="s1")
    fs = WorkspaceFileSystem()
    fs.write_text(workspace, "notes/result.txt", "hello")
    assert fs.read_text(workspace, "notes/result.txt") == "hello"
    artifact = await ArtifactStore().save_file(workspace, "notes/result.txt")
    assert artifact.workspace_id == workspace.workspace_id

@pytest.mark.asyncio
async def test_hook_runner_executes_registered_hook():
    registry = HookRegistry()

    async def handler(context: HookContext) -> HookResult:
        return HookResult(allowed=True, message="ok")

    registry.register(HookPoint.BEFORE_TOOL_CALL, "test_hook", handler)
    results = await HookRunner(registry=registry).run(
        HookContext(hook_point=HookPoint.BEFORE_TOOL_CALL, payload={"tool": "rag.search"})
    )
    assert results[0].message == "ok"

@pytest.mark.asyncio
async def test_task_runner_checkpoint():
    runner = TaskRunner()
    execution = await runner.create_execution(session_id="s1", agent_id="product_agent")
    execution = await runner.run_once(execution)
    checkpoint = await runner.checkpoint_store.latest(execution.execution_id)
    assert execution.status == "completed"
    assert checkpoint is not None
    assert checkpoint.step == 1

@pytest.mark.asyncio
async def test_event_store_and_bus():
    store = EventStore()
    bus = EventBus()
    seen = []

    async def subscriber(event: AgentEvent):
        seen.append(event.event_type)

    bus.subscribe("*", subscriber)
    event = AgentEvent(event_id="e1", event_type="tool.executed", session_id="s1", payload={"tool": "rag.search"})
    await store.append(event)
    await bus.publish(event)

    assert (await store.list_by_session("s1"))[0].event_type == "tool.executed"
    assert seen == ["tool.executed"]

@pytest.mark.asyncio
async def test_evaluation_regression_report():
    dataset = EvaluationDataset(
        name="smoke",
        cases=[EvaluationCase(case_id="c1", input="hello", expected={"contains": "ok"})],
    )
    scores = await RegressionRunner().run(dataset, outputs={"c1": {"answer": "ok"}})
    report = EvaluationReport().build(scores)
    assert report["passed"] == 1
    assert report["pass_rate"] == 1.0
