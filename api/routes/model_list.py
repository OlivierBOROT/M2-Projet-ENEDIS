# api/routes/model_list.py
import os
import boto3
from fastapi import APIRouter, HTTPException

from core.config import settings


router = APIRouter(prefix="/model_list", tags=["Model Management"])

@router.get("/")
async def list_models():
    if settings.USE_S3:
        s3 = boto3.client("s3")
        objs = s3.list_objects_v2(Bucket=settings.S3_BUCKET_NAME, Prefix="models/")
        model_files = [o["Key"].split("/")[-1] for o in objs.get("Contents", [])]
        return {"status": "success", "models": model_files}
    else:
        if not os.path.exists(settings.LOCAL_MODEL_DIR):
            return {"status": "success", "models": []}
        files = [f for f in os.listdir(settings.LOCAL_MODEL_DIR)
                 if os.path.isfile(os.path.join(settings.LOCAL_MODEL_DIR, f))]
        return {"status": "success", "models": files}
