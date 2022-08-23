from sqlalchemy import Column, String, Text
from sqlalchemy.ext.declarative import declarative_base
from core.db.mixins import TimestampMixin


Base = declarative_base()


class S3Bucket(Base, TimestampMixin):
    __tablename__ = 's3_buckets'

    id = Column(String(100), unique=True)
    key_prefix = Column(String(255), primary_key=True)
    filename = Column(String(255), primary_key=True)
    bucket_name = Column(String(255), primary_key=True)
