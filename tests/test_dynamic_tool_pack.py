import pytest
from agents.profiles import AgentRegistry
from context.caller_context import CallerContext
from context.manager import ContextManager
from tools.resolver import ToolPackBuilder

@pytest.mark.asyncio
async def test_tool_pack_builder_filters_by_agent_and_permission():
    profile = AgentRegistry.default().get("product_agent")
    caller = CallerContext(user_id="u1", department="ecommerce", roles=["operator"])
    context = ContextManager().build(
        caller=caller,
        session_id="s1",
        agent_id="product_agent",
        file_ids=[],
        short_term_memory={},
    )
    pack = await ToolPackBuilder().build(profile=profile, context=context, task_intent="product_research")
    names = {item.name for item in pack.items}
    assert "product.get_sku" in names
    assert "rag.search" in names
    assert "bi.run_readonly_sql" not in names
