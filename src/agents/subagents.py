from pydantic import BaseModel, Field

class SubAgentProfile(BaseModel):
    name: str
    role: str
    tools: list[str] = Field(default_factory=list)
    instruction: str

class SubAgentRegistry:
    def __init__(self) -> None:
        self._profiles = {
            "product_subagent": SubAgentProfile(
                name="product_subagent", role="product",
                tools=["product.get_sku", "product.search_similar"],
                instruction="负责查询商品事实、SPU/SKU、卖点、规格和相似商品。",
            ),
            "rag_subagent": SubAgentProfile(
                name="rag_subagent", role="knowledge", tools=["rag.search"],
                instruction="负责检索企业知识库，必须返回引用。",
            ),
            "data_subagent": SubAgentProfile(
                name="data_subagent", role="data", tools=["bi.run_readonly_sql"],
                instruction="负责只读数据查询和经营指标分析。",
            ),
            "order_subagent": SubAgentProfile(
                name="order_subagent", role="order", tools=["order.get_order"],
                instruction="负责查询订单和售后上下文。",
            ),
            "report_subagent": SubAgentProfile(
                name="report_subagent", role="report", tools=["bi.generate_report"],
                instruction="负责把多个子任务结果汇总成报告。",
            ),
        }

    @classmethod
    def default(cls) -> "SubAgentRegistry":
        return cls()

    def get(self, name: str) -> SubAgentProfile:
        return self._profiles[name]
