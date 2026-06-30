from pathlib import Path
import yaml
from skills.manifest import SkillManifest

class SkillRegistry:
    def __init__(self, skills_root: Path | None = None) -> None:
        self.skills_root = skills_root or Path("skills")
        self._fallback = {
            "product_copywriting": SkillManifest(name="product_copywriting", description="基于商品事实生成导购话术。", owner="product", tags=["product", "copywriting"], required_tools=["product.get_sku", "rag.search"]),
            "data_analysis": SkillManifest(name="data_analysis", description="数据分析和只读 SQL 结果解释。", owner="data", tags=["data"], required_tools=["bi.run_readonly_sql"]),
            "chart_report": SkillManifest(name="chart_report", description="把数据分析结果组织成报告结构。", owner="data", tags=["report"], required_tools=["bi.generate_report"]),
            "policy_check": SkillManifest(name="policy_check", description="售后政策检查和高风险动作约束。", owner="cs", tags=["policy", "aftersales"], required_tools=["rag.search"]),
            "citation_answer": SkillManifest(name="citation_answer", description="基于引用回答。", owner="platform", tags=["citation"], required_tools=["rag.search"]),
        }

    @classmethod
    def default(cls) -> "SkillRegistry":
        return cls()

    def get(self, name: str) -> SkillManifest:
        manifest_path = self.skills_root / name / "manifest.yaml"
        if manifest_path.exists():
            data = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}
            return SkillManifest(**data)
        if name in self._fallback:
            return self._fallback[name]
        return SkillManifest(name=name, description=f"Skill placeholder: {name}", owner="platform", enabled=True)

    def list_enabled(self) -> list[SkillManifest]:
        return [self.get(name) for name in self._fallback if self.get(name).enabled]
