import boto3
from os import getenv
from botocore.client import Config

endpoint = "https://storage.yandexcloud.net"
s3 = boto3.client(
    's3',
    endpoint_url=endpoint,
    aws_access_key_id=getenv("YANDEX_STORAGE_ACCESS_KEY"),
    aws_secret_access_key=getenv("YANDEX_STORAGE_SECRET_KEY"),
    config=Config(signature_version='s3v4')
)
bucket = getenv("YANDEX_STORAGE_BUCKET")

async def upload_to_yandex_storage(file_path: str) -> str:
    key = Path(file_path).name
    s3.upload_file(file_path, bucket, key)
    return key

async def get_presigned_url(key: str, expires_in=3600) -> str:
    return s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket, 'Key': key},
        ExpiresIn=expires_in
    )