class PromptInjectionDetector:
    def detect(self, text: str) -> bool:
        suspicious = ["ignore previous", "忽略之前", "system prompt", "developer message"]
        return any(s in text.lower() for s in suspicious)
