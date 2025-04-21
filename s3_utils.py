import boto3
import os
from dotenv import load_dotenv

load_dotenv()

def upload_to_s3(local_path, filename, bucket=None):
    bucket = bucket or os.environ["S3_BUCKET"]
    s3 = boto3.client(
        "s3",
        aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
        region_name=os.environ["AWS_REGION"]
    )

    key = f"uploads/{filename}"
    s3.upload_file(local_path, bucket, key)
    
    s3_url = f"https://rigelpdfs.s3.us-east-1.amazonaws.com/{key}"
    return s3_url
