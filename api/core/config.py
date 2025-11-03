# api/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    USE_S3: bool = False               # switch to True to use S3
    LOCAL_MODEL_DIR: str = "./app"     # local folder for models
    S3_BUCKET_NAME: str = "my-bucket"  # S3 bucket name

settings = Settings()
