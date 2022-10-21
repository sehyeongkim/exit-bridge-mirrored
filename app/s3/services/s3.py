from typing import Union, List, Dict
from enum import Enum

from sqlalchemy import select
from core.db import Transactional, Propagation, session
from core.utils.s3_uploader import BucketManager
from app.s3.models import S3Bucket
from app.user.models import User, LimitedPartnerDetail, LpApplicationForm
from app.company.models import Company
from app.union.models import MainPostDetail


class S3IdColumns(Enum):
    company_logo_img_s3_id = str(Company.logo_img_s3_id)
    company_main_banner_img_s3_id = str(Company.main_banner_img_s3_id)
    main_post_detail_attachment_json = str(MainPostDetail.attachment_json)  # {<original filename>: <s3_id>}
    user_profile_img_s3_id = str(User.profile_img_s3_id)
    limited_partner_detail_signature_img_s3_id = str(LimitedPartnerDetail.signature_img_s3_id)
    lp_application_form_signature_img_s3_id = str(LpApplicationForm.signature_img_s3_id)


class S3UrlConverter:
    def convert_to_s3_url_col_name(self, s3_id_col_name: str):
        return s3_id_col_name.replace('s3_id', 's3_url')

    async def map_from_s3_id_to_url(self, rows: Union[Dict, List[Dict]]):
        if not isinstance(rows, list):
            rows = [rows]

        s3_id_columns = [s3_id_col.value.split('.')[-1] for s3_id_col in S3IdColumns]

        dict_rows = list(map(dict, rows))
        new_mapped_rows = list()
        matched_keys = list()
        first_row = dict_rows[0]
        for k, v in first_row.items():
            if k in s3_id_columns:
                matched_keys.append(k)

        if matched_keys:
            for row in dict_rows:
                for s3_id_col_name in matched_keys:
                    s3_id = row[s3_id_col_name]
                    if not s3_id:
                        continue

                    s3_url_col_name = self.convert_to_s3_url_col_name(s3_id_col_name)
                    row[s3_url_col_name] = await S3Service().get_s3_url(s3_id)

                    del row[s3_id_col_name]
                new_mapped_rows.append(row)
        return new_mapped_rows


class S3Service(object):
    def __init__(self):
        pass

    @Transactional(propagation=Propagation.REQUIRED)
    async def create_s3_bucket_object(
            self,
            key_prefix: str,
            filename: str,
            bucket_name: str
    ) -> int:
        s3_bucket = S3Bucket(
            key_prefix=key_prefix,
            filename=filename,
            bucket_name=bucket_name
        )
        session.add(s3_bucket)
        await session.flush()
        return s3_bucket.id

    async def get_s3_bucket_object(self, s3_id) -> S3Bucket:
        result = await session.execute(select(S3Bucket).where(S3Bucket.id == s3_id))
        s3_object = result.scalars().first()
        return s3_object

    async def get_s3_url(self, s3_id) -> str:
        if 'http' in s3_id:
            return s3_id

        s3_object = await self.get_s3_bucket_object(s3_id)
        is_sensitive_bucket = BucketManager.is_sensitive_bucket(s3_object.bucket_name)
        bucket_manager = BucketManager(s3_object.key_prefix, s3_object.filename, is_sensitive_bucket)
        url = bucket_manager.get_object_read_url()
        return url
