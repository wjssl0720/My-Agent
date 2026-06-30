from agents.profiles import AgentProfile
from context.context_pack import ContextPack
from loop.models import LoadedSkill, ResolvedTool, TaskPlan

class SystemPromptBuilder:
    def build(
        self,
        *,
        profile: AgentProfile,
        context: ContextPack,
        tools: list[ResolvedTool],
        skills: list[LoadedSkill],
        task_plan: TaskPlan,
    ) -> str:
        allowed_tools = [t.name for t in tools if t.permission in ("allow", "ask")]
        denied_tools = [t.name for t in tools if t.permission == "deny"]
        skill_block = "\n".join(f"- {s.name}: {s.content}" for s in skills) or "- none"

        return f"""
你是 {profile.name}，角色是 {profile.role}。

执行原则：
1. 你必须在给出结论前优先使用可用工具获取事实。
2. RAG 是工具，不是旁路；需要知识时调用 rag.search。
3. 高风险动作必须遵守 permission / HITL。
4. 不得编造工具没有返回的商品、订单、库存、价格、销售数据。
5. 复杂任务需要拆分子任务，必要时分发给子 Agent。
6. 最终回答要解释依据，并保留可追踪结果。

调用者上下文：
- user_id: {context.caller.user_id}
- department: {context.caller.department}
- roles: {context.caller.roles}
- allowed_rag_scopes: {context.allowed_rag_scopes}

可用工具：
{allowed_tools}

禁止工具：
{denied_tools}

已加载 skills：
{skill_block}

任务计划：
{task_plan.model_dump()}
""".strip()
