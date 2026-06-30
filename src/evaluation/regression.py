from evaluation.dataset import EvaluationDataset
from evaluation.evaluator import Evaluator
from evaluation.score import EvaluationScore

class RegressionRunner:
    def __init__(self, evaluator: Evaluator | None = None) -> None:
        self.evaluator = evaluator or Evaluator()

    async def run(self, dataset: EvaluationDataset, outputs: dict[str, dict]) -> list[EvaluationScore]:
        scores = []
        for case in dataset.cases:
            output = outputs.get(case.case_id, {})
            scores.append(await self.evaluator.evaluate_case(case, output))
        return scores
