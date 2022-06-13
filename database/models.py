# coding: utf-8
from sqlalchemy import Column, Date, DateTime, Float, Integer, JSON, String, Text
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    gp_id = Column(Integer, nullable=False)
    name = Column(String(20))
    logo_img_url = Column(String(255))
    product_name = Column(String(20))
    investment_stage = Column(String(20))
    investment_method = Column(String(20))
    total_capital = Column(Float)
    total_investment = Column(Float)
    company_classification = Column(String(20))
    corporate_classification = Column(String(20))
    establishment_date = Column(Date)
    homepage_url = Column(String(255))
    business_category = Column(String(20))
    skill = Column(String(30))
    recruitment_start_date = Column(DateTime)
    recruitment_end_date = Column(DateTime)
    recruitment_status = Column(String(10))
    business_number = Column(String(30))
    venture_registration_number = Column(String(30))
    bond_issue_date = Column(Date)
    main_banner_img_url = Column(String(255))


class CompaniesLimitedPartner(Base):
    __tablename__ = 'companies_limited_partners'

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, nullable=False)
    lp_id = Column(Integer, nullable=False)


class FeedComment(Base):
    __tablename__ = 'feed_comments'

    id = Column(Integer, primary_key=True)
    user_id = Column(String(20), nullable=False)
    feed_id = Column(Integer, nullable=False)
    content = Column(String(255))
    is_secret = Column(TINYINT(1))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    mentioned_at = Column(DateTime)


class Feed(Base):
    __tablename__ = 'feeds'

    id = Column(Integer, primary_key=True)
    gp_id = Column(Integer)
    union_id = Column(Integer, nullable=False)
    company_id = Column(Integer, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)


class GeneralPartner(Base):
    __tablename__ = 'general_partners'

    id = Column(Integer, primary_key=True)
    user_id = Column(String(20), nullable=False)
    name = Column(String(20))
    date_of_birth = Column(String(20))
    applied_date = Column(DateTime)
    is_confirmed = Column(Integer)


class LimitedPartner(Base):
    __tablename__ = 'limited_partners'

    id = Column(Integer, primary_key=True)
    lp_id = Column(Integer, nullable=False)
    union_id = Column(Integer, nullable=False)
    company_id = Column(Integer, nullable=False)
    name = Column(String(20))
    registration_number = Column(String(20))
    zip_code = Column(String(10))
    road_name_address = Column(String(40))
    detailed_address = Column(String(40))
    signature_img_url = Column(String(255))
    decision_date = Column(DateTime)
    number_of_shares = Column(Integer)
    personal_info_checkbox_json = Column(JSON)
    agenda_checkbox_json = Column(JSON)
    application_checkbox_json = Column(JSON)
    income_deduction_applied_date = Column(Date)
    confirmation_status = Column(String(10))
    confirmation_date = Column(DateTime)


class LpApplicationForm(Base):
    __tablename__ = 'lp_application_forms'

    id = Column(Integer, primary_key=True)
    lp_id = Column(Integer, nullable=False)
    union_id = Column(Integer, nullable=False)
    company_id = Column(Integer, nullable=False)
    name = Column(String(20))
    registration_number = Column(String(20))
    zip_code = Column(String(10))
    road_name_address = Column(String(40))
    detailed_address = Column(String(40))
    signature_img_url = Column(String(255))
    decision_date = Column(DateTime)
    number_of_shares = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    personal_info_checkbox_json = Column(JSON)
    agenda_checkbox_json = Column(JSON)
    application_checkbox_json = Column(JSON)
    income_deduction_applied_date = Column(Date)
    confirmation_status = Column(String(10))


class MainPostQna(Base):
    __tablename__ = 'main_post_qna'

    id = Column(Integer, primary_key=True, nullable=False)
    main_post_id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(String(20), nullable=False)
    title = Column(String(40))
    content = Column(Text)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    is_answered = Column(TINYINT(1))
    answer = Column(Text)


class MainPost(Base):
    __tablename__ = 'main_posts'

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, nullable=False)
    gp_id = Column(Integer, nullable=False)
    intro = Column(Text)
    html_text = Column(Text)
    title = Column(String(40))
    inobiz_url = Column(Text)
    dart_url = Column(Text)
    is_activated = Column(TINYINT(1))
    attachment_json = Column(JSON)
    article_json = Column(JSON)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)


class Union(Base):
    __tablename__ = 'unions'

    id = Column(Integer, primary_key=True)
    gp_id = Column(Integer, nullable=False)
    company_id = Column(Integer)
    name = Column(String(20))
    unit_share_price = Column(Float)
    total_share_number = Column(Float)
    total_share_price = Column(Float)
    establishment_date = Column(DateTime)
    expire_date = Column(DateTime)
    confirmation_status = Column(String(10))


class UnionsLimitedPartner(Base):
    __tablename__ = 'unions_limited_partners'

    id = Column(Integer, primary_key=True)
    lp_id = Column(Integer, nullable=False)
    union_id = Column(Integer, nullable=False)


class User(Base):
    __tablename__ = 'users'

    id = Column(String(20), primary_key=True)
    email = Column(String(40))
    phone_number = Column(String(20))
    type = Column(String(10))
    access_token = Column(String(255))
    refresh_token = Column(String(255))
    profile_img_url = Column(String(255))
    is_verified = Column(Integer)
    zip_code = Column(String(10))
    road_name_address = Column(String(40))
    detailed_address = Column(String(40))
