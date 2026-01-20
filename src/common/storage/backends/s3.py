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


class S3Storage:
    """
    S3 storage backend.
    """

    def read_parquet(self, key: str) -> pd.DataFrame:
        bucket = _bucket(key)
        resp = _s3().get_object(Bucket=bucket, Key=key)
        buf = io.BytesIO(resp["Body"].read())
        return pd.read_parquet(buf)
    
    def write_parquet(self, df: pd.DataFrame, key: str, **kwargs) -> None:
        bucket = _bucket(key)
        buf = io.BytesIO()
        df.to_parquet(buf, **kwargs)
        buf.seek(0)
        _s3().put_object(Bucket=bucket, Key=key, Body=buf.read())
    
    def read_bytes(self, key: str) -> bytes:
        bucket = _bucket(key)
        resp = _s3().get_object(Bucket=bucket, Key=key)
        return resp["Body"].read()
    
    def write_bytes(self, data: bytes, key: str) -> None:
        bucket = _bucket(key)
        _s3().put_object(Bucket=bucket, Key=key, Body=data)
    
    def exists(self, key: str) -> bool:
        bucket = _bucket(key)
        try:
            _s3().head_object(Bucket=bucket, Key=key)
            return True
        except ClientError as e:
            return False