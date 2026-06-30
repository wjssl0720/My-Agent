from evaluation.dataset import EvaluationCase
from evaluation.score import EvaluationScore

class Evaluator:
    async def evaluate_case(self, case: EvaluationCase, output: dict) -> EvaluationScore:
        passed = True
        expected_contains = case.expected.get("contains")
        if expected_contains:
            passed = expected_contains in str(output)
        return EvaluationScore(case_id=case.case_id, passed=passed, score=1.0 if passed else 0.0)
