from uuid import uuid4
from agents.profiles import AgentProfile
from loop.models import TaskItem, TaskPlan

class TaskPlanner:
    def plan(self, profile: AgentProfile, message: str) -> TaskPlan:
        text = message.lower()

        if "转化" in message or "下降" in message or "conversion" in text:
            return TaskPlan(
                is_complex=True,
                goal=message,
                tasks=[
                    TaskItem(task_id=str(uuid4()), description="查询商品基础信息", assignee="product_subagent"),
                    TaskItem(task_id=str(uuid4()), description="检索运营分析 SOP 和商品知识", assignee="rag_subagent"),
                    TaskItem(task_id=str(uuid4()), description="查询销售/转化相关只读指标", assignee="data_subagent"),
                    TaskItem(task_id=str(uuid4()), description="汇总原因和建议动作", assignee="report_subagent"),
                ],
            )

        if "报表" in message or "销售" in message or "sql" in text:
            return TaskPlan(is_complex=False, goal=message, tasks=[
                TaskItem(task_id=str(uuid4()), description="执行只读数据查询", assignee="data_agent")
            ])

        if "退款" in message or "refund" in text:
            return TaskPlan(is_complex=False, goal=message, tasks=[
                TaskItem(task_id=str(uuid4()), description="判断退款动作是否需要 HITL", assignee="aftersales_agent")
            ])

        return TaskPlan(is_complex=False, goal=message, tasks=[
            TaskItem(task_id=str(uuid4()), description="检索知识并回答", assignee=profile.agent_id)
        ])
