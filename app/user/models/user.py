from sqlalchemy import Column, Boolean, String, Integer, JSON, DateTime, Text, Date

from core.db import Base
from core.db.mixins import TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = 'users'

    id = Column(String(20), primary_key=True)  # uuid first + last part -> length 20
    kakao_user_id = Column(String(50), unique=True)  # index
    email = Column(String(40))
    phone_number = Column(String(20))
    type = Column(String(10))
    access_token = Column(String(255))
    refresh_token = Column(String(255))
    profile_img_url = Column(Text)
    is_verified = Column(Boolean, default=False)
    zip_code = Column(String(10))
    road_name_address = Column(String(40))
    detailed_address = Column(String(40))


class GeneralPartner(Base, TimestampMixin):
    __tablename__ = 'general_partners'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(20), nullable=False)
    nickname = Column(String(50))
    name = Column(String(20))
    date_of_birth = Column(String(20))
    applied_date = Column(DateTime)
    confirmation_date = Column(DateTime)
    year_of_gp_experience = Column(Integer)


class GeneralPartnerCareer(Base):
    __tablename__ = 'general_partner_careers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    gp_id = Column(Integer, nullable=False)
    career_start_date = Column(Date)
    career_end_date = Column(Date)
    worked_company = Column(String(50))
    worked_position_description = Column(Text)


class GeneralPartnerUnionEstablishmentExperience(Base):
    __tablename__ = 'general_partner_union_establishment_experiences'

    id = Column(Integer, primary_key=True, autoincrement=True)
    gp_id = Column(Integer, nullable=False)
    union_start_date = Column(Date)
    union_end_date = Column(Date)
    union_id_certificate_url = Column(Text)
    union_investment_certificate_url = Column(Text)


class LimitedPartner(Base):
    __tablename__ = 'limited_partners'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    union_id = Column(Integer, nullable=False)
    company_id = Column(Integer, nullable=False)
    name = Column(String(20))
    confirmation_date = Column(DateTime)


class LimitedPartnerDetail(Base, TimestampMixin):
    __tablename__ = 'limited_partner_details'

    id = Column(Integer, primary_key=True, autoincrement=True)
    lp_id = Column(Integer)  # index
    registration_number = Column(String(20))
    zip_code = Column(String(10))
    road_name_address = Column(String(40))
    detailed_address = Column(String(40))
    signature_img_url = Column(Text)
    decision_date = Column(DateTime)
    total_share_number = Column(Integer)
    personal_info_checkbox_json = Column(JSON)
    agenda_checkbox_json = Column(JSON)
    application_checkbox_json = Column(JSON)
    income_deduction_applied_date = Column(Integer)


class LpApplicationForm(Base, TimestampMixin):
    __tablename__ = 'lp_application_forms'

    id = Column(Integer, primary_key=True, autoincrement=True)
    lp_id = Column(Integer, nullable=False)
    union_id = Column(Integer, nullable=False)
    company_id = Column(Integer, nullable=False)
    name = Column(String(20))
    registration_number = Column(String(20))
    zip_code = Column(String(10))
    road_name_address = Column(String(40))
    detailed_address = Column(String(40))
    signature_img_url = Column(Text)
    decision_date = Column(DateTime)
    total_share_number = Column(Integer)
    personal_info_checkbox_json = Column(JSON)
    agenda_checkbox_json = Column(JSON)
    application_checkbox_json = Column(JSON)
    income_deduction_applied_date = Column(Integer)
    confirmation_status = Column(String(10))
    reject_reason = Column(Text)
