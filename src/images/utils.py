from fastapi import FastAPI, File, UploadFile
import boto3
import os




ACCESS_KEY = 't5m6mqmtkup61qhe'
SECRET_KEY = "364ce769-6036-44db-b2e3-30d5502f5fb2"
ENDPOINT_URL = 'https://storage.c2.liara.space'
BUCKET_NAME = 'admiring-proskuriakova-u6--ascny'

s3_client = boto3.client(
    "s3",
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    endpoint_url=ENDPOINT_URL,
)