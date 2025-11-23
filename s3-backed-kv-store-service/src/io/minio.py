from src.io.base import BaseClient
from minio import Minio
from src.config import minio_settings


class MinioClient(BaseClient):
    def __init__(self):
        self.client = Minio(minio_settings.ENDPOINT, access_key=minio_settings.ACCESS_KEY, secret_key=minio_settings.SECRET_KEY)
        self.bucket = minio_settings.BUCKET

    def get_object(self, key: str) -> bytes:
        return self.client.get_object(Bucket=self.bucket, Key=key)["Body"].read()

    def put_object(self, key: str, value: bytes) -> None:
        self.client.put_object(Bucket=self.bucket, Key=key, Body=value)
