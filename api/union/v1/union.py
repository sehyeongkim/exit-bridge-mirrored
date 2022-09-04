from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from app.union.schemas import *
from app.union.services import UnionService
from app.user.services import GPService
from core.fastapi.dependencies import PermissionDependency, IsGP, get_gp_id
from core.exceptions.union import *
from core.utils.logger import debugger


union_router = APIRouter()


@union_router.post(
    '',
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsGP]))]
)
async def register_union(union_request: UnionRegistrationRequestSchema, gp_id: int = Depends(get_gp_id)):
    if await UnionService().is_union_name_duplicated(union_request.union_name):
        raise UnionNameDuplicatedException

    await UnionService().create_union(
        gp_id,
        **union_request.dict()
    )
    return JSONResponse(content={'result': 'SUCCESS'}, status_code=200)


@union_router.get(
    "/gp/union/status",
    responses={
        "400": {"model": ExceptionResponseSchema},
        "200": {"model": UnionOverallResponseSchema}
    },
    dependencies=[Depends(PermissionDependency([IsGP]))]
)
async def get_overall_union_status(gp_id: int = Depends(get_gp_id)):
    unions = await UnionService().get_unions(gp_id)
    union_historical_status = await UnionService().get_union_historical_status(gp_id)
    union_summary = await UnionService().get_union_summary(gp_id)
    result = {
        'result': {
            'unions': unions,
            'union_historical_status': union_historical_status,
            'union_summary': union_summary
        }
    }
    return JSONResponse(content=jsonable_encoder(result), status_code=200)
