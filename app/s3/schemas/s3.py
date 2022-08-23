from pydantic import BaseModel, Field


class S3UploadRequestSchema(BaseModel):
    key_prefix: str = Field(..., description='S3 Prefix (디렉토리)')
    filename: str = Field(..., description='S3 파일명 (디렉토리 부분 제외한 object key name)', length=254)
