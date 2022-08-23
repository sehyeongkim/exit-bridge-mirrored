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


class Bucket:
    class Sensitive:
        bucket_name = config.AWS_S3_SENSITIVE_BUCKET_NAME
        bucket_domain_url = None

    class Public:
        bucket_name = config.AWS_S3_PUBLIC_BUCKET_NAME
        bucket_domain_url = config.AWS_S3_PUBLIC_BUCKET_CLOUDFRONT_DOMAIN_NAME


class KeyPrefix:
    class Sensitive(Enum):
        gp = 'gp'
        lp = 'lp'

    class Public(Enum):
        company = 'company'
        feed = 'feed'


class BucketManager:
    def __init__(self, key_prefix, filename):
        self.key_prefix = key_prefix
        self.filename = filename
        self.object_key_name = f'{key_prefix}/{filename}'
        self.s3_client_manager = S3ClientManager()

    @property
    def bucket_name(self):
        bucket_object = self.get_bucket_object()
        if bucket_object:
            return bucket_object.bucket_name
        return None

    @staticmethod
    def get_key_prefix_by_object_key_name(object_key_name):
        return object_key_name.lower().split('/')[0]

    def get_bucket_object(self):
        if self.key_prefix in KeyPrefix.Sensitive.__members__:
            return Bucket.Sensitive

        elif self.key_prefix in KeyPrefix.Public.__members__:
            return Bucket.Public
        return None

    def get_object_url_for_read(self):
        bucket_object = self.get_bucket_object()
        if isinstance(bucket_object, Bucket.Sensitive):
            url = self.s3_client_manager.get_presigned_url(
                ClientMethods.get_object,
                bucket_object.bucket_name,
                self.object_key_name,
                config.AWS_S3_SENSITIVE_FILE_DOWNLOAD_EXPIRE_SECONDS
            )
        elif isinstance(bucket_object, Bucket.Public):
            url = f'{bucket_object.bucket_domain_url}/{self.object_key_name}'
        else:
            raise
        return url

    def get_object_url_for_upload(self):
        bucket_object = self.get_bucket_object()
        url = self.s3_client_manager.get_presigned_url(
            ClientMethods.put_object,
            bucket_object.bucket_name,
            self.object_key_name,
            config.AWS_S3_SENSITIVE_FILE_UPLOAD_EXPIRE_SECONDS
        )
        return url


class S3ClientManager:
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
            bucket_name,
            object_full_path: str,
            expires_in: int
    ) -> str:
        url = self.client.generate_presigned_url(
            ClientMethod=client_method,
            Params={'Bucket': bucket_name, 'Key': object_full_path},
            ExpiresIn=expires_in
        )
        return url
