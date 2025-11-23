import boto3
from src.config import settings


class S3Client:
    def __init__(self):
        self.client = boto3.client("s3")
        self.bucket = settings.S3_BUCKET

    def get_object(self, key: str) -> bytes:
        return self.client.get_object(Bucket=self.bucket, Key=key)["Body"].read()

    def put_object(self, key: str, value: bytes) -> None:
        self.client.put_object(Bucket=self.bucket, Key=key, Body=value)
