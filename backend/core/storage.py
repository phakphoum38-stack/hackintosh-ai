import boto3
import os

s3 = boto3.client(
    "s3",
    region_name=os.getenv("AWS_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)

BUCKET = os.getenv("AWS_BUCKET")


def upload_file(file_path: str, key: str) -> str:
    if not os.path.exists(file_path):
        raise Exception(f"File not found: {file_path}")

    s3.upload_file(file_path, BUCKET, key)

    return f"https://{BUCKET}.s3.{os.getenv('AWS_REGION')}.amazonaws.com/{key}"
