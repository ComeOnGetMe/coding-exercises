from src.config import settings
from src.io.s3 import S3Client
from src.io.local import LocalClient


def get_storage_client():
    if settings.STORAGE_BACKEND == "s3":
        return S3Client()
    elif settings.STORAGE_BACKEND == "local":
        return LocalClient(storage_dir=settings.LOCAL_STORAGE_DIR)
    else:
        raise ValueError(f"Invalid storage backend: {settings.STORAGE_BACKEND}")
