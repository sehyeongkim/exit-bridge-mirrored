import datetime as dt

from sqlalchemy import or_, select, update, delete, func
from sqlalchemy.sql.expression import Subquery

from app.union.models import *
from app.company.models import Company
from core.db import Transactional, Propagation, session
from app.union.schemas import UnionStatus


class UnionService(object):
    def __init__(self):
        pass

    async def sub_get_lps_by_gp(self, gp_id: int) -> Subquery:
        sub_unions = select(Union.id).where(Union.gp_id == gp_id).subquery()
        sub_lps = select(
            sub_unions.c.id.label('union_id'),
            func.count(UnionsLimitedPartner.lp_id).label('total_lp_number')
        ).join(
            sub_unions, UnionsLimitedPartner.union_id == sub_unions.c.id
        ).group_by(
            sub_unions.c.id
        ).subquery()
        return sub_lps

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

    async def get_unions(self, gp_id: int) -> list:
        sub_lps = self.sub_get_lps_by_gp(gp_id)
        stmt = select(
            Union.id,
            Union.gp_id,
            Union.company_id,
            Company.name.label('company_name'),
            Union.name.label('union_name'),
            Union.establishment_date,
            Union.expire_date,
            Union.status.label('confirmation_status'),
            sub_lps.c.total_lp_number,
            Union.total_share_price
        ).join(
            sub_lps, Union.id == sub_lps.c.union_id
        ).join(
            Company, Union.company_id == Company.id
        )
        result = await session.execute(stmt)
        return result.scalars().all()

    async def get_union_historical_status(self, gp_id: int) -> dict:
        stmt = select(
            func.count(Union.id).label('unions_number'),
            Union.status
        ).where(
            Union.gp_id == gp_id
        ).group_by(
            Union.status
        )
        result = await session.execute(stmt)
        return result.scalars().first()

    async def get_union_summary(self, gp_id: int) -> dict:
        sub_lps = self.sub_get_lps_by_gp(gp_id)
        stmt = select(
            func.sum(Union.total_share_price).label('AUM'),
            func.count(Union.company_id).label('total_company_number'),
            func.count(Union.id).label('total_union_number'),
            func.sum(sub_lps.c.total_lp_number).label('total_lp_number')
        ).join(
            sub_lps, Union.id == sub_lps.c.union_id
        )
        result = await session.execute(stmt)
        return result.scalars().first()

    async def get_unions_detail_information(self, gp_id: int) -> list:
        stmt = select(
            Union.id,
            Union.name.label('union_name'),
            Union.gp_id,
            Union.company_id,
            Union.unit_share_price,
            Union.total_share_number,
            Union.total_share_price,
            Union.establishment_date,
            Union.expire_date,
            Union.status.label('confirmation_status')
        ).where(Union.gp_id == gp_id)
        result = await session.execute(stmt)
        return result.scalars().all()