from pathlib import Path
from uuid import uuid4
from fastapi import UploadFile
from context.caller_context import CallerContext

class FileService:
    def __init__(self, base_dir: Path | None = None) -> None:
        self.base_dir = base_dir or Path("/tmp/ecom_agent_uploads")
        self.base_dir.mkdir(parents=True, exist_ok=True)

    @classmethod
    def default(cls) -> "FileService":
        return cls()

    async def save_upload(self, file: UploadFile, caller: CallerContext) -> dict:
        file_id = str(uuid4())
        suffix = Path(file.filename or "").suffix
        path = self.base_dir / f"{file_id}{suffix}"
        content = await file.read()
        path.write_bytes(content)
        return {
            "file_id": file_id,
            "filename": file.filename,
            "size": len(content),
            "owner_user_id": caller.user_id,
            "storage_path": str(path),
        }
