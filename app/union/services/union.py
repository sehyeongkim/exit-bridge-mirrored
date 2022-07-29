import datetime as dt

from sqlalchemy import or_, select, update, delete
from app.union.models import *
from core.db import Transactional, Propagation, session
from app.union.schemas import UnionStatus


class UnionService(object):
    def __init__(self):
        pass

    @Transactional(propagation=Propagation.REQUIRED)
    async def create_union(
            self,
            gp_id: int,
            union_name: str,
            unit_share_price: float,
            total_share_number: float,
            total_share_price: float,
            establishment_date: dt.datetime,
            expire_date: dt.datetime,
            status: UnionStatus
    ) -> Union:
        union = Union(
            gp_id=gp_id,
            name=union_name,
            unit_share_price=unit_share_price,
            total_share_number=total_share_number,
            total_share_price=total_share_price,
            establishment_date=establishment_date,
            expire_date=expire_date,
            status=status
        )
        session.add(union)
        await session.flush()
        return union

    async def is_union_name_duplicated(self, union_name) -> bool:
        result = await session.execute(select(Union).where(Union.name == union_name))
        union = result.scalars().first()
        if union:
            return True
        return False
