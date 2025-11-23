import os
from pydantic_settings import BaseSettings
from pydantic import Field


class MinIOSettings(BaseSettings):
    ENDPOINT: str = os.getenv("MINIO_ENDPOINT", "localhost:9000")
    ACCESS_KEY: str = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
    SECRET_KEY: str = os.getenv("MINIO_SECRET_KEY", "minioadmin")
    BUCKET: str = os.getenv("MINIO_BUCKET", "example-bucket")

class S3Settings(BaseSettings):
    BUCKET: str = os.getenv("S3_BUCKET", "example-bucket")

class LocalStorageSettings(BaseSettings):
    DIR: str = os.getenv("LOCAL_STORAGE_DIR", "./storage")

class LoggingSettings(BaseSettings):
    LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    FORMAT: str = os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    DATE_FORMAT: str = os.getenv("LOG_DATE_FORMAT", "%Y-%m-%d %H:%M:%S")

class MetricsSettings(BaseSettings):
    ENABLE: bool = os.getenv("ENABLE_METRICS", "false").lower() == "true"


class ServiceSettings(BaseSettings):
    STORAGE_BACKEND: str = os.getenv("STORAGE_BACKEND", "local")
    PORT: int = int(os.getenv("PORT", "8000"))

    metrics_settings: MetricsSettings = Field(default_factory=MetricsSettings)
    logging_settings: LoggingSettings = Field(default_factory=LoggingSettings)


settings = ServiceSettings()
minio_settings = MinIOSettings()
s3_settings = S3Settings()
local_storage_settings = LocalStorageSettings()
