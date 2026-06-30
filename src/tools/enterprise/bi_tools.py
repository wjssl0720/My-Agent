from context.context_pack import ContextPack
from safety.sql_guard import assert_readonly_sql
from tools.base import ToolSpec

class RunReadonlySqlTool:
    spec = ToolSpec(name="bi.run_readonly_sql", description="执行只读 SQL", risk_level="high")

    async def execute(self, args: dict, context: ContextPack) -> dict:
        sql = args.get("sql", "")
        assert_readonly_sql(sql)
        return {
            "columns": ["dt", "mock_value"],
            "rows": [["2026-06-30", 1]],
            "sql": sql,
            "source": "mock_bi",
        }

class GenerateReportTool:
    spec = ToolSpec(name="bi.generate_report", description="生成报表", risk_level="medium")

    async def execute(self, args: dict, context: ContextPack) -> dict:
        return {
            "title": "示例经营分析报告",
            "sections": ["销售概览", "商品表现", "建议动作"],
            "source": "mock_bi",
        }
