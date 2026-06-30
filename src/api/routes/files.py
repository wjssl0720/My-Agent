from fastapi import APIRouter, Depends, UploadFile, File
from api.deps import get_caller_context
from context.caller_context import CallerContext
from files.service import FileService

router = APIRouter(tags=["files"])
file_service = FileService.default()

@router.post("/files")
async def upload_file(
    file: UploadFile = File(...),
    caller: CallerContext = Depends(get_caller_context),
) -> dict:
    return await file_service.save_upload(file=file, caller=caller)
