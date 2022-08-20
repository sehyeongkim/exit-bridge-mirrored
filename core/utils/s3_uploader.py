import boto3

from botocore.config import Config
from enum import Enum
from fastapi import File
from core.config import config


S3_CONFIG = Config(
    region_name=config.AWS_S3_REGION_NAME,
    signature_version='s3v4'
)


class ClientMethods(Enum):
    get_object = 'get_object'
    put_object = 'put_object'


class Buckets:
    sensitive = config.AWS_S3_SENSITIVE_BUCKET_NAME
    public = config.AWS_S3_PUBLIC_BUCKET_NAME


class KeyPrefix:
    class Sensitive(Enum):
        gp = 'gp'
        lp = 'lp'

    class NonSensitive(Enum):
        company = 'company'
        feed = 'feed'


class BucketManager:
    @staticmethod
    def get_key_prefix_by_object_key_name(object_key_name):
        return object_key_name.lower().split('/')[0]

    @staticmethod
    def get_bucket_by_key_prefix(key_prefix):
        if key_prefix in KeyPrefix.Sensitive.__members__:
            return Buckets.sensitive

        elif key_prefix in KeyPrefix.NonSensitive.__members__:
            return Buckets.public
        return None


class S3UpDownLoader:
    def __init__(self):
        self.client = boto3.client(
            's3',
            aws_access_key_id=config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
            config=S3_CONFIG
        )

    async def upload_file(self, file_path: str, file: File):
        self.client.upload_fileobj(file.file, config.AWS_S3_SENSITIVE_BUCKET_NAME, file_path)

    def get_presigned_url(
            self,
            client_method: ClientMethods,
            object_key_name: str,
            expires_in: int
    ) -> str:
        key_prefix = BucketManager.get_key_prefix_by_object_key_name(object_key_name)
        bucket_name = BucketManager.get_bucket_by_key_prefix(key_prefix)

        url = self.client.generate_presigned_url(
            ClientMethod=client_method,
            Params={'Bucket': bucket_name, 'Key': object_key_name},
            ExpiresIn=expires_in
        )
        return url
