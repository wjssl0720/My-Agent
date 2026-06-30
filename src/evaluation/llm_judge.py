from evaluation.dataset import EvaluationCase
from evaluation.score import EvaluationScore

class LlmJudge:
    async def judge(self, case: EvaluationCase, output: dict) -> EvaluationScore:
        # 占位：生产中接 LLM judge。
        return EvaluationScore(case_id=case.case_id, passed=True, score=1.0, reason="mock judge")
