from fastapi import APIRouter, Depends, Query, Request

from app.user.schemas import *
from core.fastapi.dependencies import (
    PermissionDependency,
    IsAuthenticated
)
from core.config import config
from core.utils.s3_uploader import S3UpDownLoader, ClientMethods


s3_router = APIRouter()


@s3_router.post(
    '/s3',
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))]
)
async def upload_to_s3(
        file_path: str = Form(..., description="s3 bucket file path"),
        file: UploadFile = File(..., description="file")
):
    result = await S3UpDownLoader().upload_file(file_path, file)
    return result


@s3_router.post(
    '/s3/presigned-url',
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))]
)
async def get_s3_presigned_url_for_upload(
        object_key_name: str = Form(..., description='object key name, equivalent to full filepath')
):
    url = S3UpDownLoader().get_presigned_url(
        ClientMethods.put_object.value,
        object_key_name,
        config.AWS_S3_SENSITIVE_FILE_UPLOAD_EXPIRE_SECONDS
    )
    return {'result': url}
