import datetime as dt

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from app.company.schemas import *
from app.company.schemas.company import CompanyRegistrationRequestSchema
from app.company.services import CompanyService
from app.user.services import GPService

from core.fastapi.dependencies import PermissionDependency, IsGP, get_gp_id
from core.exceptions.user import AuthorizationMismatchedException
from core.utils.logger import debugger

company_router = APIRouter()


@company_router.post(
    '',
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsGP]))]
)
async def register_company(company_request: CompanyRegistrationRequestSchema, gp_id: int = Depends(get_gp_id)):
    if company_request.recruitment_status == RecruitmentStatus.OPEN.value:
        CompanyRegistrationRequestSchema.recruitment_start_date = dt.datetime.now().date()

    await CompanyService().create_company(
        gp_id,
        **company_request.dict(),
    )
    return {'result': 'SUCCESS'}


@company_router.get(
    '/search',
    responses={'400': {'model': ExceptionResponseSchema},
               '200': {'model': CompanyPostResponseSchema}}
)
async def get_companies_post(q: Optional[str] = None):
    posts = await CompanyService().get_post_of_companies(q)
    opened, closed = [], []
    for post in posts:
        if post['is_open_to_public']:
            opened.append(post)
        else:
            closed.append(post)
        del post['is_open_to_public']

    result = {
        'result': {
            'open': opened,
            'closed': closed
        }
    }
    return JSONResponse(content=jsonable_encoder(result), status_code=200)


@company_router.get(
    '/post',
    responses={'400': {'model': ExceptionResponseSchema},
               '200': {'model': CompanyPostResponseSchema}}
)
async def get_main_post(main_post_id: int):
    main_post = await CompanyService().get_main_post(main_post_id)
    result = {
        'result': main_post
    }
    return JSONResponse(content=jsonable_encoder(result), status_code=200)