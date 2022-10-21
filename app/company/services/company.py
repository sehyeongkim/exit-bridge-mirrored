import datetime as dt
import typing

from sqlalchemy import or_, select, update, delete
from app.union.models import *
from app.company.models import *
from app.s3.services import S3UrlConverter
from core.db import Transactional, Propagation, session


class CompanyService(object):
    def __init__(self):
        pass

    @Transactional(propagation=Propagation.REQUIRED)
    async def create_company(
            self,
            gp_id: int,
            union_id: int,
            company_name: str,
            logo_img_url: str,
            product_name: str,
            investment_stage: str,
            investment_method: str,
            total_capital: float,
            total_investment: float,
            company_classification: str,
            corporate_classification: str,
            establishment_date: dt.datetime,
            homepage_url: str,
            business_category: str,
            skill: str,
            business_number: str,
            venture_registration_number: str,
            bond_issue_date: dt.datetime,
            main_banner_img_url: str,
            main_post_title: str,
            main_post_intro: str,
            main_post_html_text: str,
            attachment_json: list,
            article_json: dict,
            recruitment_status: str,
            is_open_to_public: bool,
            recruitment_start_date: typing.Union[dt.datetime, None]
    ) -> None:
        company = Company(
            gp_id=gp_id,
            union_id=union_id,
            name=company_name,
            logo_img_url=logo_img_url,
            product_name=product_name,
            investment_stage=investment_stage,
            investment_method=investment_method,
            total_capital=total_capital,
            total_investment=total_investment,
            company_classification=company_classification,
            corporate_classification=corporate_classification,
            establishment_date=establishment_date,
            homepage_url=homepage_url,
            business_category=business_category,
            skill=skill,
            business_number=business_number,
            venture_registration_number=venture_registration_number,
            bond_issue_date=bond_issue_date,
            main_banner_img_url=main_banner_img_url
        )
        session.add(company)
        await session.flush()

        main_post_detail = MainPostDetail(
            html_text=main_post_html_text,
            attachment_json=attachment_json,
            article_json=article_json
        )
        session.add(main_post_detail)
        await session.flush()

        main_post = MainPost(
            main_post_detail_id=main_post_detail.id,
            company_id=company.id,
            gp_id=gp_id,
            intro=main_post_intro,
            title=main_post_title,
            recruitment_status=recruitment_status,
            recruitment_start_date=recruitment_start_date,
            is_open_to_public=is_open_to_public
        )
        session.add(main_post)

    async def get_post_of_companies(self, q: str or None) -> list:
        stmt = select(
            Company.id.label('company_id'),
            Company.name.label('company_name'),
            Company.logo_img_s3_id,
            MainPost.id.label('main_post_id'),
            Company.main_banner_img_s3_id,
            MainPost.intro,
            MainPost.is_open_to_public
        ).join(
            MainPost, Company.id == MainPost.company_id
        )
        if q is not None:
            stmt = stmt.where(Company.name.like(f'%{q}%'))
        result = await session.execute(stmt)
        rows = result.all()
        mapped_rows = await S3UrlConverter().map_from_s3_id_to_url(rows)
        return mapped_rows

    async def get_main_post(self, main_post_id: int) -> dict:
        stmt = select(
            MainPost.company_id,
            Company.name.label('company_name'),
            MainPost.intro,
            MainPost.title,
            MainPost.is_open_to_public.label('is_activated'),
            Company.logo_img_s3_id,
            Company.main_banner_img_s3_id,
            MainPost.updated_at,
            MainPost.recruitment_start_date,
            MainPost.recruitment_end_date,
            MainPostDetail.html_text,
            MainPostDetail.inobiz_url,
            MainPostDetail.dart_url,
            MainPostDetail.attachment_json,
            MainPostDetail.article_json
        ).join(
            Company, MainPost.company_id == Company.id
        ).join(
            MainPostDetail, MainPost.main_post_detail_id == MainPostDetail.id
        ).where(
            MainPost.id == main_post_id
        )
        result = await session.execute(stmt)
        row = result.one()
        mapped_rows = await S3UrlConverter().map_from_s3_id_to_url(row)
        return mapped_rows[0]
