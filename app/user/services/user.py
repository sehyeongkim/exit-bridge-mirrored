import uuid

from typing import Optional, List, Union, NoReturn

from sqlalchemy import or_, select

from app.user.models import User
from core.db import Transactional, Propagation, session


class UserService:
    def __init__(self):
        pass

    async def get_user_list(self, limit: int = 12, prev: Optional[int] = None,) -> List[User]:
        query = select(User)

        if prev:
            query = query.where(User.id < prev)

        if limit > 12:
            limit = 12

        query = query.limit(limit)
        result = await session.execute(query)
        return result.scalars().all()

    async def get_user_by_kakao_user_id(self, kakao_user_id: str) -> Union[User, None]:
        result = await session.execute(
            select(User).where(User.kakao_user_id == kakao_user_id)
        )
        user = result.scalars().first()
        return user if user else None

    @Transactional(propagation=Propagation.REQUIRED)
    async def create_user(self, kakao_user_id: str, name: str, phone_number: str) -> User:
        random_id = str(uuid.uuid4()).split('-')
        user_id = random_id[0] + random_id[-1]
        user = User(
            id=user_id,
            kakao_user_id=kakao_user_id,
            name=name,
            phone_number=phone_number
        )
        session.add(user)
        return user

    async def is_admin(self, user_id: str) -> bool:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()
        if not user:
            return False

        if user.type.lower() == 'admin':
            return True
        return False

    async def is_gp(self, user_id: str) -> bool:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()
        if not user:
            return False

        if user.type.lower() == 'gp':
            return True
        return False
