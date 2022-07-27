from sqlalchemy import Column, String, Integer, Float, DateTime

from core.db import Base
from core.db.mixins import TimestampMixin


class Union(Base, TimestampMixin):
    __tablename__ = 'unions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    gp_id = Column(Integer, nullable=False)
    company_id = Column(Integer)
    name = Column(String(20), unique=True)
    unit_share_price = Column(Float)
    total_share_number = Column(Float)
    total_share_price = Column(Float)
    establishment_date = Column(DateTime)
    expire_date = Column(DateTime)
    status = Column(String(10))


class UnionsLimitedPartner(Base):
    __tablename__ = 'unions_limited_partners'

    id = Column(Integer, primary_key=True, autoincrement=True)
    lp_id = Column(Integer, nullable=False)
    union_id = Column(Integer, nullable=False)
