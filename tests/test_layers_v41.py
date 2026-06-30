import pytest
from agents.profiles import AgentRegistry
from context.caller_context import CallerContext
from context.manager import ContextManager
from mcp.server_registry import McpServerRegistry
from rag.schemas import RagQuery
from rag.service import RagService
from skills.loader import SkillLoader
from skills.registry import SkillRegistry
from tools.providers.mcp_provider import McpToolProvider
from tools.providers.skill_provider import SkillToolProvider

def test_skill_registry_loads_manifest():
    manifest = SkillRegistry.default().get("product_copywriting")
    assert manifest.name == "product_copywriting"
    assert "product.get_sku" in manifest.required_tools

def test_skill_loader_loads_skill_md():
    skill = SkillLoader().load_one("product_copywriting")
    assert skill.name == "product_copywriting"
    assert "Product Copywriting Skill" in skill.content

@pytest.mark.asyncio
async def test_rag_service_acl_filter():
    result = await RagService.default().search(RagQuery(query="财务制度", allowed_scopes=["finance_docs"]))
    assert result.chunks
    assert all(chunk.scope == "finance_docs" for chunk in result.chunks)

@pytest.mark.asyncio
async def test_mcp_registry_disabled_by_default():
    registry = McpServerRegistry.default()
    assert registry.list_servers(enabled_only=True) == []
    assert registry.list_servers(enabled_only=False)

@pytest.mark.asyncio
async def test_mcp_provider_returns_empty_when_servers_disabled():
    profile = AgentRegistry.default().get("product_agent")
    caller = CallerContext(user_id="u1", department="ecommerce", roles=["operator"])
    context = ContextManager().build(caller=caller, session_id="s1", agent_id="product_agent", file_ids=[], short_term_memory={})
    candidates = await McpToolProvider().list_candidates(profile=profile, context=context, task_intent=None)
    assert candidates == []

@pytest.mark.asyncio
async def test_skill_provider_currently_does_not_expose_tool_candidates():
    profile = AgentRegistry.default().get("product_agent")
    caller = CallerContext(user_id="u1", department="ecommerce", roles=["operator"])
    context = ContextManager().build(caller=caller, session_id="s1", agent_id="product_agent", file_ids=[], short_term_memory={})
    candidates = await SkillToolProvider().list_candidates(profile=profile, context=context, task_intent=None)
    assert candidates == []
