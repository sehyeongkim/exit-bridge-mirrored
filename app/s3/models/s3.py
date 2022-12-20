from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from core.db.mixins import TimestampMixin


Base = declarative_base()


class S3Bucket(Base, TimestampMixin):
    __tablename__ = 's3_buckets'
    id = Column(Integer, primary_key=True, autoincrement=True)
    key_prefix = Column(String(255))
    filename = Column(String(255))
    bucket_name = Column(String(255))
