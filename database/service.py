from sqlalchemy.future import select
from database.models import User


class BaseModel(object):
    def __init__(self, session):
        self.session = session


class UserService(BaseModel):
    async def get_user(self, user_id):
        stmt = select(User).where(User.id == user_id)
        user = await self.session.execute(stmt)
        return user.scalar()
