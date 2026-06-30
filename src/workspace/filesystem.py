from pathlib import Path
from workspace.models import Workspace

class WorkspaceFileSystem:
    def write_text(self, workspace: Workspace, relative_path: str, content: str) -> str:
        path = Path(workspace.base_path) / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return str(path)

    def read_text(self, workspace: Workspace, relative_path: str) -> str:
        path = Path(workspace.base_path) / relative_path
        return path.read_text(encoding="utf-8")

    def list_files(self, workspace: Workspace) -> list[str]:
        base = Path(workspace.base_path)
        return [str(path.relative_to(base)) for path in base.rglob("*") if path.is_file()]
