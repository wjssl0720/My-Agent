from evaluation.score import EvaluationScore

class FailureAnalysis:
    def analyze(self, scores: list[EvaluationScore]) -> list[dict]:
        return [
            {"case_id": score.case_id, "reason": score.reason}
            for score in scores
            if not score.passed
        ]
