from pathlib import Path
from uuid import uuid4
from workspace.models import Artifact, Workspace

class ArtifactStore:
    def __init__(self) -> None:
        self._artifacts: dict[str, Artifact] = {}

    async def save_file(self, workspace: Workspace, relative_path: str, artifact_type: str = "file") -> Artifact:
        artifact_id = str(uuid4())
        path = Path(workspace.base_path) / relative_path
        artifact = Artifact(
            artifact_id=artifact_id,
            workspace_id=workspace.workspace_id,
            path=str(path),
            artifact_type=artifact_type,
        )
        self._artifacts[artifact_id] = artifact
        return artifact

    async def get(self, artifact_id: str) -> Artifact | None:
        return self._artifacts.get(artifact_id)
