import os
import boto3
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

MODEL_PATH = "/app/model_cache"
MODEL_BUCKET = "rigelclausenet"
MODEL_PREFIX = "rigel-model/"

def download_from_s3():
    if not os.path.exists(MODEL_PATH):
        os.makedirs(MODEL_PATH)

    s3 = boto3.client(
        "s3",
        aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
        region_name=os.environ["AWS_REGION"]
    )

    files = s3.list_objects_v2(Bucket=MODEL_BUCKET, Prefix=MODEL_PREFIX).get("Contents", [])
    for obj in files:
        key = obj["Key"]
        filename = os.path.join(MODEL_PATH, os.path.basename(key))
        if not os.path.exists(filename):
            s3.download_file(MODEL_BUCKET, key, filename)

_model = None
_tokenizer = None

def get_model():
    global _model, _tokenizer
    if _model is None or _tokenizer is None:
        download_from_s3()
        _tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
        _model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
    return _model, _tokenizer
