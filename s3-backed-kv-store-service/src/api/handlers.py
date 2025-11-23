from fastapi import HTTPException
from botocore.exceptions import ClientError
from src.io import get_storage_client
from src.utils import setup_logging

logger = setup_logging()
storage_client = get_storage_client()


def read(key: str) -> str:
    try:
        logger.info(f"Reading key: {key}")
        payload = storage_client.get_object(key)
        # Return raw value, not JSON parsed
        return payload.decode("utf-8")
    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code", "")
        if error_code == "NoSuchKey":
            raise HTTPException(status_code=404, detail=f"Key '{key}' not found")
        raise HTTPException(status_code=500, detail=str(e))


def write(key: str, value: str) -> int:
    try:
        logger.info(f"Writing key: {key} with value: {value}")
        # Store raw value as bytes
        payload = value.encode("utf-8")
        storage_client.put_object(key, payload)
        return len(payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
