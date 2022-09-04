import uuid

from fastapi import APIRouter, Depends

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
async def get_s3_presigned_url_for_upload(request: S3UploadRequestSchema):
    bucket_manager = BucketManager(request.key_prefix, request.filename)
    url = bucket_manager.get_object_url_for_upload()
    return {'result': url}


@s3_router.post(
    '/upload/presigned-url/after-upload',
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))]
)
async def get_s3_id_after_upload(request: S3UploadRequestSchema):
    s3_id = str(uuid.uuid4())
    bucket_manager = BucketManager(request.key_prefix, request.filename)
    await S3Service().create_s3_bucket_object(
        s3_id,
        request.key_prefix,
        request.filename,
        bucket_manager.bucket_name
    )
    return {'result': s3_id}
