import pytest
from context.caller_context import CallerContext
from context.manager import ContextManager
from memory.memory_manager import MemoryManager

@pytest.mark.asyncio
async def test_memory_manager_short_term_roundtrip():
    manager = MemoryManager.default()
    await manager.append_short_term("s1", {"user": "hello"})
    data = await manager.short_term.load("s1")
    assert data["history"][0]["user"] == "hello"

@pytest.mark.asyncio
async def test_memory_manager_load_for_context():
    caller = CallerContext(user_id="u1", department="ecommerce", roles=["operator"])
    context = ContextManager().build(
        caller=caller,
        session_id="s1",
        agent_id="product_agent",
        file_ids=[],
        short_term_memory={},
    )
    manager = MemoryManager.default()
    result = await manager.load_for_context(context)
    assert "short_term" in result
    assert "long_term" in result
