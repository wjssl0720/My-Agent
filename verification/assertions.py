def assert_tool_called(tool_calls: list[dict], tool_name: str) -> None:
    called = {t["tool_name"] for t in tool_calls}
    assert tool_name in called, f"Expected tool {tool_name}, got {called}"

def assert_tool_not_called(tool_calls: list[dict], tool_name: str) -> None:
    called = {t["tool_name"] for t in tool_calls}
    assert tool_name not in called, f"Unexpected tool {tool_name}"

def assert_tool_status(tool_calls: list[dict], tool_name: str, status: str) -> None:
    for call in tool_calls:
        if call["tool_name"] == tool_name:
            assert call["status"] == status, f"{tool_name} expected {status}, got {call['status']}"
            return
    raise AssertionError(f"Tool {tool_name} not found")

def assert_event_exists(events: list[dict], event_type: str) -> None:
    types = {e["type"] for e in events}
    assert event_type in types, f"Expected event {event_type}, got {types}"

def assert_subagent_dispatched(events: list[dict], subagent_name: str) -> None:
    dispatched = [e["payload"].get("subagent_name") for e in events if e["type"] == "subagent.dispatched"]
    assert subagent_name in dispatched, f"Expected subagent {subagent_name}, got {dispatched}"

def assert_citation_title(citations: list[dict], title: str) -> None:
    titles = {c["title"] for c in citations}
    assert title in titles, f"Expected citation title {title}, got {titles}"
