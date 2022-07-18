import requests

from typing import List, Dict, Type
from fastapi import APIRouter, Depends, Query

from app.user.schemas import (
    ExceptionResponseSchema,
    GetUserListResponseSchema,
    UserLoginRequestSchema,
    UserLoginResponseSchema,
)
from app.user.services import UserService
from core.fastapi.dependencies import (
    PermissionDependency,
    IsAdmin,
)
from core.config import config
from core.exceptions.user import *
from core.utils.logger import debugger
from core.utils.token_helper import TokenHelper


user_router = APIRouter()


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
        if request.phone_number and request.name:
            create_user_dict = dict(
                kakao_user_id=kakao_user_id,
                name=request.name,
                phone_number=request.phone_number
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


