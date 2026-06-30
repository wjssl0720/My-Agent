from evaluation.score import EvaluationScore

class EvaluationReport:
    def build(self, scores: list[EvaluationScore]) -> dict:
        total = len(scores)
        passed = sum(1 for score in scores if score.passed)
        return {
            "total": total,
            "passed": passed,
            "pass_rate": passed / total if total else 0.0,
            "scores": [score.model_dump() for score in scores],
        }
