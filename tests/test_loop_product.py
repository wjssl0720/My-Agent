import pytest
from context.caller_context import CallerContext
from context.manager import ContextManager
from runtime.base import RuntimeInput
from runtime.loop_runtime import LoopRuntime

@pytest.mark.asyncio
async def test_loop_calls_product_and_rag():
    caller = CallerContext(user_id="u1", department="ecommerce", roles=["operator"])
    context = ContextManager().build(
        caller=caller,
        session_id="s1",
        agent_id="product_agent",
        file_ids=[],
        short_term_memory={},
    )
    out = await LoopRuntime.local_harness().invoke(
        RuntimeInput(message="查询 SKU 商品并生成导购话术", agent_id="product_agent", context=context)
    )
    names = [c.tool_name for c in out.tool_calls]
    assert "product.get_sku" in names
    assert "rag.search" in names
    assert any(e.type == "prompt.built" for e in out.events)
