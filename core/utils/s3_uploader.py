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


class BucketManager:
    def __init__(self, key_prefix: str, filename: str, is_sensitive_bucket: bool):
        self.key_prefix = key_prefix
        self.filename = filename
        self.object_key_name = f'{key_prefix}/{filename}'
        self.s3_client_manager = S3ClientManager()
        self.is_sensitive_bucket = is_sensitive_bucket

    @property
    def bucket_name(self):
        bucket_object = self.get_bucket_object()
        return bucket_object.bucket_name

    @staticmethod
    def get_separte_object_key_paths(object_key_name) -> tuple:
        splited_object_key_name = object_key_name.lower().split('/')
        join_paths = splited_object_key_name[:-1]
        filename = splited_object_key_name[-1]

        if not join_paths:
            return object_key_name, filename

        key_prefix = '/'.join(join_paths)
        return key_prefix, filename

    @property
    def get_bucket_object(self):
        if self.is_sensitive_bucket:
            return Bucket.Sensitive
        else:
            return Bucket.Public

    @staticmethod
    def is_sensitive_bucket(bucket_name):
        if bucket_name == Bucket.Public.bucket_name:
            return False
        elif bucket_name == Bucket.Sensitive.bucket_name:
            return True

    def get_object_read_url(self):
        bucket_object = self.get_bucket_object
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

    def get_object_upload_url(self):
        bucket_object = self.get_bucket_object()
        url = self.s3_client_manager.get_presigned_url(
            ClientMethods.put_object.value,
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
