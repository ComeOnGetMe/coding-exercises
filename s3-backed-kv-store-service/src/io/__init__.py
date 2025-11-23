from src.config import settings
from src.io.s3 import S3Client
from src.io.local import LocalClient
from src.io.minio import MinioClient


def get_storage_client():
    match settings.STORAGE_BACKEND:
        case "s3":
            return S3Client()
        case "local":
            return LocalClient()
        case "minio":
            return MinioClient()
        case _:
            raise ValueError(f"Invalid storage backend: {settings.STORAGE_BACKEND}")
