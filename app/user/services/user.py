import uuid
import datetime as dt
import typing

from typing import Optional, List
from sqlalchemy import or_, select, update, delete

from app.user.models import *
from app.user.schemas import GPCareer, UnionEstablishmentExperience, UserType
from core.db import Transactional, Propagation, session


class UserService(object):
    def __init__(self):
        pass

    async def get_user_list(self, limit: int = 12, prev: Optional[int] = None, ) -> List[User]:
        query = select(User)

        if prev:
            query = query.where(User.id < prev)

        if limit > 12:
            limit = 12

        query = query.limit(limit)
        result = await session.execute(query)
        return result.scalars().all()

    async def get_user_by_kakao_user_id(self, kakao_user_id: str) -> typing.Union[User, None]:
        result = await session.execute(
            select(User).where(User.kakao_user_id == kakao_user_id)
        )
        user = result.scalars().first()
        return user if user else None

    async def get_user_by_id(self, user_id: str) -> typing.Union[User, None]:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()
        if not user:
            return None
        return user

    @Transactional(propagation=Propagation.REQUIRED)
    async def create_user(self, kakao_user_id: str, phone_number: str, email: str) -> str:
        random_id = str(uuid.uuid4()).split('-')
        user_id = random_id[0] + random_id[-1]
        user = User(
            id=user_id,
            kakao_user_id=kakao_user_id,
            phone_number=phone_number,
            email=email
        )
        session.add(user)
        await session.flush()
        return user.id

    async def is_admin(self, user_id: str) -> bool:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()
        if not user:
            return False

        if user.type.lower() == UserType.ADMIN.value:
            return True
        return False

    async def is_gp(self, user_id: str) -> bool:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()
        if not user:
            return False

        if user.type.lower() == UserType.GP.value:
            return True
        return False

    @Transactional()
    async def delete_user(self, user_id) -> None:
        await session.execute(delete(User).where(User.id == user_id))

    async def get_user_by_email(self, email) -> User:
        result = await session.execute(
            select(User).where(User.email == email)
        )
        user = result.scalars().first()
        return user if user else None


class GPService(object):
    def __init__(self):
        pass

    @Transactional(propagation=Propagation.REQUIRED)
    async def create_gp_application(
            self,
            user_id: str,
            nickname: str,
            name: str,
            registration_number: str,
            zip_code: str,
            road_name_address: str,
            detailed_address: str,
            applied_date: dt.date,
            year_of_gp_experience: int,
            careers: List[GPCareer],
            union_establishment_experiences: List[UnionEstablishmentExperience]
    ) -> None:
        query = update(User).values(
            name=name,
            registration_number=registration_number,
            zip_code=zip_code,
            road_name_address=road_name_address,
            detailed_address=detailed_address
        ).where(User.id == user_id)
        await session.execute(query)

        result = await session.execute(select(GeneralPartner).where(GeneralPartner.user_id == user_id))
        gp = result.scalars().first()
        if not gp:
            gp = GeneralPartner(
                user_id=user_id,
                nickname=nickname,
                applied_date=applied_date,
                year_of_gp_experience=year_of_gp_experience
            )
            session.add(gp)
            await session.flush()

        await session.execute(delete(GeneralPartnerCareer).where(GeneralPartnerCareer.gp_id == gp.id))
        for each in careers:
            each = GPCareer.parse_obj(each)
            gp_career = GeneralPartnerCareer(
                gp_id=gp.id,
                career_start_date=each.career_start_date,
                career_end_date=each.career_end_date,
                worked_company=each.worked_company,
                worked_position_description=each.worked_position_description
            )
            session.add(gp_career)

        await session.execute(
            delete(GeneralPartnerUnionEstablishmentExperience) \
                .where(GeneralPartnerUnionEstablishmentExperience.gp_id == gp.id)
        )
        for each in union_establishment_experiences:
            each = UnionEstablishmentExperience.parse_obj(each)
            gp_union_establishment_experience = GeneralPartnerUnionEstablishmentExperience(
                gp_id=gp.id,
                union_start_date=each.union_start_date,
                union_end_date=each.union_end_date,
                union_id_certificate_url=each.union_id_certificate_url,
                union_investment_certificate_url=each.union_investment_certificate_url
            )
            session.add(gp_union_establishment_experience)

    async def is_gp_nickname_duplicated(self, gp_nickname) -> bool:
        result = await session.execute(select(GeneralPartner).where(GeneralPartner.nickname == gp_nickname))
        nickname = result.scalars().first()
        if nickname:
            return True
        return False

    async def get_gp_id(self, user_id: str) -> int:
        result = await session.execute(select(GeneralPartner.id).where(GeneralPartner.user_id == user_id))
        gp_id = result.scalars().first()
        return gp_id

    async def get_gp(self, gp_id) -> GeneralPartner:
        result = await session.execute(select(GeneralPartner).where(GeneralPartner.id == gp_id))
        gp = result.scalars().first()
        return gp

    @Transactional(propagation=Propagation.REQUIRED)
    async def approve_gp(self, gp_id: str, confirmation_date: dt.datetime) -> None:
        result = await session.execute(select(GeneralPartner).where(GeneralPartner.id == gp_id))
        gp = result.scalars().first()
        gp.confirmation_date = confirmation_date

        user_query = update(User) \
            .values(type=UserType.GP.value) \
            .where(User.id == gp.user_id)
        await session.execute(user_query)
