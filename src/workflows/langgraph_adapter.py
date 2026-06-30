class LangGraphWorkflowAdapter:
    async def run_workflow(self, workflow_name: str, payload: dict) -> dict:
        return {"workflow_name": workflow_name, "payload": payload, "status": "not_implemented"}
