from config import S3_BUCKET_NAME, s3
from botocore.exceptions import NoCredentialsError, ClientError

def list_files(fileName):
    try:
        file_names_list = fileName.split(',')
        response = s3.list_objects_v2(Bucket=S3_BUCKET_NAME)
        matching_files = [
            obj for obj in response['Contents']
            if obj['Key'] in file_names_list
        ]
        return matching_files
    except (NoCredentialsError, ClientError) as e:
        return []

def upload_files(file):
    if not file.filename.endswith('.pdf'):
        return None
    try:
        # Upload the file to S3
        s3.upload_fileobj(file.file, S3_BUCKET_NAME, file.filename)
        return file.filename
    except (NoCredentialsError, ClientError) as e:
        # Handle errors related to AWS credentials or S3 client
        print(f"Error uploading file to S3: {e}")
        return None
