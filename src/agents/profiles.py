from pydantic import BaseModel, Field

class AgentProfile(BaseModel):
    agent_id: str
    name: str
    role: str
    base_prompt_name: str
    tools: list[str] = Field(default_factory=list)
    skills: list[str] = Field(default_factory=list)
    subagents: list[str] = Field(default_factory=list)

class AgentRegistry:
    def __init__(self) -> None:
        self._profiles = {
            "knowledge_agent": AgentProfile(
                agent_id="knowledge_agent", name="企业知识 Agent", role="knowledge",
                base_prompt_name="knowledge_agent", tools=["rag.search"],
                skills=["citation_answer"], subagents=[],
            ),
            "product_agent": AgentProfile(
                agent_id="product_agent", name="商品导购 Agent", role="product",
                base_prompt_name="product_agent",
                tools=["product.get_sku", "product.search_similar", "rag.search"],
                skills=["product_copywriting", "citation_answer"],
                subagents=["product_subagent", "rag_subagent", "data_subagent", "report_subagent"],
            ),
            "data_agent": AgentProfile(
                agent_id="data_agent", name="数据分析 Agent", role="data",
                base_prompt_name="data_agent",
                tools=["bi.run_readonly_sql", "bi.generate_report", "rag.search"],
                skills=["data_analysis", "chart_report"],
                subagents=["data_subagent", "report_subagent"],
            ),
            "aftersales_agent": AgentProfile(
                agent_id="aftersales_agent", name="售后 Agent", role="aftersales",
                base_prompt_name="aftersales_agent",
                tools=["order.get_order", "order.refund", "rag.search"],
                skills=["policy_check", "citation_answer"],
                subagents=["order_subagent", "rag_subagent"],
            ),
        }

    @classmethod
    def default(cls) -> "AgentRegistry":
        return cls()

    def get(self, agent_id: str) -> AgentProfile:
        return self._profiles.get(agent_id, self._profiles["knowledge_agent"])
