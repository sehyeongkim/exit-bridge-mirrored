from pydantic import BaseModel, Field


class S3UploadRequestSchema(BaseModel):
    is_sensitive_bucket: bool = Field(..., description='민감버킷 여부')


class S3UploadSuccessRequestSchema(BaseModel):
    object_key_name: str = Field(..., description='object key name (파일 경로)')
    is_sensitive_bucket: bool = Field(..., description='민감버킷 여부')
