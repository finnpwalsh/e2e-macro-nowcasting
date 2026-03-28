"""S3 Implementation of Storage."""
from __future__ import annotations

import io
import os
from typing import Any

import boto3
import pandas as pd
from botocore.exceptions import ClientError

# helpers
def _bucket(key: str) -> str:
    if key.startswith("data/"):
        b = os.getenv("AWS_S3_BUCKET_DATA")
    elif key.startswith("artifacts/"):
        b = os.getenv("AWS_S3_BUCKET_ARTIFACTS")
    else:
        raise ValueError(f"Key must start with 'data/' or 'artifacts/': {key}")

    if not b:
        raise RuntimeError("Missing required env var for S3 bucket.")
    return b

def _s3() -> Any:
    region = os.getenv("AWS_S3_REGION", "us-east-1")
    return boto3.client("s3", region_name=region)

def _is_not_found_error(exc: ClientError) -> bool:
    code = exc.response.get("Error", {}).get("Code")
    return code in {"NoSuchKey", "404", "NotFound"}


class S3Storage:
    """
    S3 storage backend.
    """

    def read_parquet(self, key: str) -> pd.DataFrame:
        data = self.read_bytes(key)
        buf = io.BytesIO(data)
        return pd.read_parquet(buf)
    
    def write_parquet(self, key: str, df: pd.DataFrame, **kwargs) -> None:
        bucket = _bucket(key)
        buf = io.BytesIO()
        df.to_parquet(buf, **kwargs)
        buf.seek(0)
        _s3().put_object(Bucket=bucket, Key=key, Body=buf.read())
    
    def read_bytes(self, key: str) -> bytes:
        bucket = _bucket(key)
        try:
            resp = _s3().get_object(Bucket=bucket, Key=key)
        except ClientError as e:
            if _is_not_found_error(e):
                raise FileNotFoundError(f"s3://{bucket}/{key}") from e
            raise
        return resp["Body"].read()
    
    def write_bytes(self, key: str, data: bytes) -> None:
        bucket = _bucket(key)
        _s3().put_object(Bucket=bucket, Key=key, Body=data)
    
    def exists(self, key: str) -> bool:
        bucket = _bucket(key)
        try:
            _s3().head_object(Bucket=bucket, Key=key)
            return True
        except ClientError as e:
            if _is_not_found_error(e):
                return False
            raise