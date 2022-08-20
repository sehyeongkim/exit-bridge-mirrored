import requests

from typing import Dict
from fastapi import APIRouter, Depends, Query, Request

from app.user.schemas import *
from app.user.services import UserService, GPService
from core.fastapi.dependencies import (
    PermissionDependency,
    IsAdmin,
    IsAuthenticated
)
from core.config import config
from core.exceptions.user import *
from core.utils.logger import debugger
from core.utils.token_helper import TokenHelper
from core.utils.s3_uploader import S3UpDownLoader, ClientMethods


user_router = APIRouter()


@user_router.get('/auth-key')
async def get_authkey(request: Request, user_type: str = 'admin'):
    token_helper = TokenHelper()
    token = token_helper.encode({'user_id': 2 if user_type == 'admin' else 1})
    return {'Authorization': f'bearer {token}'}


# example code
@user_router.get(
    "",
    response_model=List[GetUserListResponseSchema],
    response_model_exclude={"id"},
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAdmin]))],
)
async def get_user_list(
        limit: int = Query(10, description="Limit"),
        prev: int = Query(None, description="Prev ID"),
):
    return await UserService().get_user_list(limit=limit, prev=prev)


@user_router.post(
    '/login',
    response_model=Dict[str, UserLoginResponseSchema],
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def signup_kakao_user(request: UserLoginRequestSchema):
    headers = {'Authorization': f'Bearer {request.kakao_access_token}'}
    response = requests.get(config.KAKAO_USERINFO_REQUEST_URL, headers=headers).json()
    code = response.get('code', None)
    msg = response.get('msg', None)

    if isinstance(code, int):
        if code == -401:
            if 'exist' in msg:
                debugger.debug(f'kakao access token not exist: {msg}')
                raise KakaoAccessTokenNotExistException
            elif 'ip' in msg:
                debugger.debug(f'kakao ip mismatched: {msg}')
                raise KakaoIpMismatchedException
        elif code == -1:
            debugger.debug(f'kakao server temporary error: {msg}')
            raise KakaoServerTemporaryErrorException
        else:
            debugger.exception(f'kakao token unknown error: {response}')
            raise

    kakao_user_id = response['id']
    user = await UserService().get_user_by_kakao_user_id(kakao_user_id)
    if not user:
        if request.phone_number and request.email:
            create_user_dict = dict(
                kakao_user_id=kakao_user_id,
                phone_number=request.phone_number,
                email=request.email
            )
            user = await UserService().create_user(**create_user_dict)
        else:
            raise KakaoUserIdNotRegisteredException

    token_payload = dict(
        user_id=user.id,
        kakao_user_id=user.kakao_user_id,
        email=user.email,
        phone_number=user.phone_number
    )
    user_access_token = TokenHelper().encode(token_payload)
    result = dict(
        access_token=user_access_token,
        kakao_user_id=kakao_user_id,
        user_id=user.id
    )
    return {'result': result}


@user_router.post(
    '/gp/application',
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))]
)
async def register_gp_application(request: Request, gp_application_request: GPApplicationRequestSchema):
    await GPService().create_gp_application(
        request.user.id,
        **gp_application_request.dict()
    )
    return {'result': 'SUCCESS'}


@user_router.post(
    '/gp/approve',
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAdmin]))]
)
async def approve_gp(request: Request, gp_id):
    gp = await GPService().get_gp(gp_id)
    if not gp:
        raise GPNotFoundException

    confirmation_date = dt.datetime.now()
    await GPService().approve_gp(
        gp_id,
        confirmation_date
    )
    return {'result': 'SUCCESS'}


@user_router.post(
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


@user_router.post(
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
