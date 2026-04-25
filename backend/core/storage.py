import os
import boto3

AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET = os.getenv("S3_BUCKET")

s3 = boto3.client(
    "s3",
    region_name=AWS_REGION,
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)


def upload_file(local_path: str, s3_key: str):

    s3.upload_file(
        local_path,
        S3_BUCKET,
        s3_key,
        ExtraArgs={"ACL": "public-read"}  # หรือเอาออกถ้า private
    )

    return f"https://{S3_BUCKET}.s3.{AWS_REGION}.amazonaws.com/{s3_key}"
