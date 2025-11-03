# api/routes/model_upload.py
import os
import shutil
import boto3
from fastapi import APIRouter, UploadFile, File, HTTPException

from core.config import settings

router = APIRouter(prefix="/post_new_model", tags=["Model Management"])

@router.post("/")
async def post_new_model(file: UploadFile = File(...)):
    try:
        if settings.USE_S3:
            s3 = boto3.client("s3")
            s3.upload_fileobj(file.file, settings.S3_BUCKET_NAME, f"models/{file.filename}")
            return {"status": "success", "message": f"{file.filename} uploaded to S3"}
        else:
            os.makedirs(settings.LOCAL_MODEL_DIR, exist_ok=True)
            save_path = os.path.join(settings.LOCAL_MODEL_DIR, file.filename)
            with open(save_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            return {"status": "success", "message": f"{file.filename} uploaded locally"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
