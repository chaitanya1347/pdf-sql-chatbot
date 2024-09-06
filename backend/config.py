import boto3
from dotenv import load_dotenv
import os

load_dotenv()


AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Initialize the S3 client
s3 = boto3.client('s3',
                    aws_access_key_id = AWS_ACCESS_KEY,
                    aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
                     )