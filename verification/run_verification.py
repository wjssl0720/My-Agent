import asyncio
from pathlib import Path
import yaml
from rich.console import Console
from context.caller_context import CallerContext
from core.models import SendMessageRequest
from runtime.orchestrator import AgentOrchestrator
from verification.assertions import (
    assert_citation_title,
    assert_event_exists,
    assert_subagent_dispatched,
    assert_tool_called,
    assert_tool_not_called,
    assert_tool_status,
)

console = Console()

async def run_case(path: Path) -> bool:
    case = yaml.safe_load(path.read_text(encoding="utf-8"))
    caller = CallerContext(**case["caller"])
    req = SendMessageRequest(message=case["input"], agent_id=case["agent_id"])
    orchestrator = AgentOrchestrator.default_for_verification()
    resp = await orchestrator.invoke(session_id=case["session_id"], req=req, caller=caller)

    tool_calls = [t.model_dump() for t in resp.tool_calls]
    events = [e.model_dump() for e in resp.events]
    citations = [c.model_dump() for c in resp.citations]
    expected = case.get("expected", {})

    try:
        for event_type in expected.get("must_have_events", []):
            assert_event_exists(events, event_type)
        for tool in expected.get("must_call_tools", []):
            assert_tool_called(tool_calls, tool)
        for tool in expected.get("must_not_call_tools", []):
            assert_tool_not_called(tool_calls, tool)
        for tool, status in expected.get("must_have_status", {}).items():
            assert_tool_status(tool_calls, tool, status)
        for subagent in expected.get("must_dispatch_subagents", []):
            assert_subagent_dispatched(events, subagent)
        for title in expected.get("must_have_citation_titles", []):
            assert_citation_title(citations, title)

        console.print(f"[green]PASS[/green] {case['id']}")
        return True
    except Exception as exc:
        console.print(f"[red]FAIL[/red] {case['id']}: {exc}")
        console.print("tool_calls=", tool_calls)
        console.print("events=", events)
        console.print("citations=", citations)
        return False

async def main() -> None:
    cases = sorted(Path("verification/cases").glob("*.yaml"))
    results = [await run_case(path) for path in cases]
    passed = sum(results)
    total = len(results)
    console.print(f"pass_rate={passed / total:.2%} ({passed}/{total})")
    if passed != total:
        raise SystemExit(1)

if __name__ == "__main__":
    asyncio.run(main())
