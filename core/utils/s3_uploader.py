import boto3

from core.config import config

from fastapi import File


class S3UpDownLoader:
    def __init__(self):
        self.client = boto3.client('s3', aws_access_key_id=config.AWS_ACCESS_KEY_ID, aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY)

    async def upload_file(self, file_path: str, file: File):
        self.client.upload_fileobj(file.file, config.AWS_S3_BUCKET_NAME, file_path)

    async def download_file(self):
        pass
