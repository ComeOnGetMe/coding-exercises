from src.io.base import BaseClient
from minio import Minio
from minio.error import S3Error
from io import BytesIO
from src.config import minio_settings


class MinioClient(BaseClient):
    def __init__(self):
        self.client = Minio(
            minio_settings.ENDPOINT,
            access_key=minio_settings.ACCESS_KEY,
            secret_key=minio_settings.SECRET_KEY,
            secure=False  # Set to True if using HTTPS
        )
        self.bucket = minio_settings.BUCKET
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        """Ensure the bucket exists, create it if it doesn't."""
        try:
            if not self.client.bucket_exists(self.bucket):
                self.client.make_bucket(self.bucket)
        except S3Error as e:
            raise IOError(f"Failed to ensure bucket '{self.bucket}' exists: {str(e)}")

    def get_object(self, key: str) -> bytes:
        try:
            response = self.client.get_object(self.bucket, key)
            data = response.read()
            response.close()
            response.release_conn()
            return data
        except S3Error as e:
            raise IOError(f"Failed to get object '{key}': {str(e)}")

    def put_object(self, key: str, value: bytes) -> None:
        try:
            data_stream = BytesIO(value)
            self.client.put_object(
                self.bucket,
                key,
                data_stream,
                length=len(value)
            )
        except S3Error as e:
            raise IOError(f"Failed to put object '{key}': {str(e)}")
