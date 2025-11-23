import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    STORAGE_BACKEND: str = os.getenv("STORAGE_BACKEND", "local")
    LOCAL_STORAGE_DIR: str = os.getenv("STORAGE_DIR", "./storage")
    S3_BUCKET: str = os.getenv("S3_BUCKET", "example-bucket")

    PORT: int = int(os.getenv("PORT", "8000"))

    ENABLE_METRICS: bool = os.getenv("ENABLE_METRICS", "false").lower() == "true"

    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    LOG_DATE_FORMAT: str = os.getenv("LOG_DATE_FORMAT", "%Y-%m-%d %H:%M:%S")


settings = Settings()
