class BaseMcpServer:
    name: str = "base"
    async def list_tools(self) -> list[dict]:
        return []
    async def call_tool(self, tool_name: str, arguments: dict) -> dict:
        return {"tool_name": tool_name, "arguments": arguments, "status": "not_implemented"}
