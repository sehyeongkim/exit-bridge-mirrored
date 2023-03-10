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


user_router = APIRouter()


@user_router.get(
    '/auth-key',
    responses={"500": {"model": ExceptionResponseSchema},
               "422": {"model": RequestValidationExceptionResponseSchema}}
)
async def get_authkey(email: str):
    user = await UserService().get_user_by_email(email)

    token_helper = TokenHelper()
    token = token_helper.encode({'user_id': user.id})
    return {'Authorization': f'bearer {token}'}


# example code
@user_router.get(
    "",
    response_model=List[GetUserListResponseSchema],
    response_model_exclude={"id"},
    responses={"500": {"model": ExceptionResponseSchema},
               "422": {"model": RequestValidationExceptionResponseSchema}},
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
    responses={"500": {"model": ExceptionResponseSchema},
               "422": {"model": RequestValidationExceptionResponseSchema}},
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
            user_id = await UserService().create_user(**create_user_dict)
            user = await UserService().get_user_by_id(user_id)
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
    responses={"500": {"model": ExceptionResponseSchema},
               "422": {"model": RequestValidationExceptionResponseSchema}},
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
    responses={"500": {"model": ExceptionResponseSchema},
               "422": {"model": RequestValidationExceptionResponseSchema}},
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


@user_router.delete(
    '/delete-account',
    responses={"500": {"model": ExceptionResponseSchema},
               "422": {"model": RequestValidationExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))]
)
async def delete_user(request: Request):
    await UserService().delete_user(request.user.id)
    return {'result': 'SUCCESS'}
