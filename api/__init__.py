from fastapi import APIRouter

from api.user.v1.user import user_router as user_v1_router
from api.company.v1.company import company_router as company_v1_router
from api.union.v1.union import union_router as union_v1_router
from api.s3.v1.s3 import s3_router as s3_v1_router, s3_router

router = APIRouter()
router.include_router(user_v1_router, prefix="/api/v1/users", tags=["User"])
router.include_router(company_v1_router, prefix="/api/v1/companies", tags=["Company"])
router.include_router(union_v1_router, prefix="/api/v1/unions", tags=["Union"])
router.include_router(s3_router, prefix="/api/v1/s3", tags=["S3"])


__all__ = ["router"]
