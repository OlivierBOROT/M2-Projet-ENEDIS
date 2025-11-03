# api/routes/model_download.py

import os
import tempfile
import boto3

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from core.config import settings

router = APIRouter(prefix="/download_model", tags=["Model Management"])

@router.get("/{filename}")
async def download_model(filename: str):
    if settings.USE_S3:
        try:
            s3 = boto3.client("s3")
            tmp_file = tempfile.NamedTemporaryFile(delete=False)
            s3.download_file(settings.S3_BUCKET_NAME, f"models/{filename}", tmp_file.name)
            return FileResponse(tmp_file.name, filename=filename)
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))
    else:
        path = os.path.join(settings.LOCAL_MODEL_DIR, filename)
        if not os.path.exists(path):
            raise HTTPException(status_code=404, detail="Model not found")
        return FileResponse(path, filename=filename)
