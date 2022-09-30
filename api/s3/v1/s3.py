import uuid

from fastapi import APIRouter, Depends, Request

from app.user.schemas import *
from app.s3.schemas import *
from app.s3.services import S3Service
from core.fastapi.dependencies import (
    PermissionDependency,
    IsAuthenticated
)
from core.utils.s3_uploader import BucketManager, S3ClientManager


s3_router = APIRouter()


@s3_router.post(
    '/upload/file',
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))]
)
async def upload_to_s3(
        file_path: str = Form(..., description="s3 bucket file path"),
        file: UploadFile = File(..., description="file")
):
    result = await S3ClientManager().upload_file(file_path, file)
    return result


@s3_router.post(
    '/upload/presigned-url',
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))]
)
async def get_s3_presigned_url_for_upload(request: Request, s3_upload: S3UploadRequestSchema):
    random_filename = str(uuid.uuid4())
    bucket_manager = BucketManager(request.user.id, random_filename, s3_upload.is_sensitive_bucket)
    url = bucket_manager.get_object_upload_url()
    result = dict(
        presigned_url=url,
        object_key_name=bucket_manager.object_key_name,
        is_sensitive_bucket=s3_upload.is_sensitive_bucket
    )
    return {'result': result}


@s3_router.post(
    '/upload/presigned-url/after-upload',
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))]
)
async def get_s3_id_after_upload(request: S3UploadSuccessRequestSchema):
    key_prefix, filename = BucketManager.get_separte_object_key_paths(request.object_key_name)

    bucket_manager = BucketManager(key_prefix, filename, request.is_sensitive_bucket)
    s3_id = await S3Service().create_s3_bucket_object(
        key_prefix,
        filename,
        bucket_manager.bucket_name
    )
    result = dict(
        s3_id=s3_id
    )
    return {'result': result}
