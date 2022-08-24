from sqlalchemy import or_, select, update, delete
from core.db import Transactional, Propagation, session
from core.utils.s3_uploader import BucketManager
from app.s3.models.s3 import S3Bucket


class S3Service(object):
    def __init__(self):
        pass

    @Transactional(propagation=Propagation.REQUIRED)
    async def create_s3_bucket_object(
            self,
            s3_id: str,
            key_prefix: str,
            filename: str,
            bucket_name: str
    ) -> None:
        s3_bucket = S3Bucket(
            id=s3_id,
            key_prefix=key_prefix,
            filename=filename,
            bucket_name=bucket_name
        )
        session.add(s3_bucket)

    async def get_s3_bucket_object(self, s3_id) -> S3Bucket:
        result = await session.execute(select(S3Bucket).where(S3Bucket.id == s3_id))
        s3_object = result.scalars().first()
        return s3_object

    async def get_s3_url(self, s3_id) -> str:
        s3_object = await self.get_s3_bucket_object(s3_id)
        bucket_manager = BucketManager(s3_object.key_prefix, s3_object.filename)
        url = bucket_manager.get_object_url_for_read()
        return url
