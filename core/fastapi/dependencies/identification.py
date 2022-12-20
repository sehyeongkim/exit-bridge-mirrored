from fastapi import Request
from app.user.services import GPService


async def get_gp_id(request: Request) -> int:
    gp_id = await GPService().get_gp_id(request.user.id)
    return gp_id
