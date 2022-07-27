from fastapi import APIRouter, Depends, Request

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
    return {'result': 'SUCCESS'}
