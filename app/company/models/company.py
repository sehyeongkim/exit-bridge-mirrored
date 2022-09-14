from sqlalchemy import Column, Date, DateTime, Float, Integer, String, Text, null
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True, autoincrement=True)
    gp_id = Column(Integer, nullable=False)
    union_id = Column(Integer, nullable=False)
    name = Column(String(20))
    logo_img_url = Column(Text)
    product_name = Column(String(20))
    investment_stage = Column(String(20))
    investment_method = Column(String(20))
    total_capital = Column(Float)
    total_investment = Column(Float)
    company_classification = Column(String(20))
    corporate_classification = Column(String(20))
    establishment_date = Column(Date)
    homepage_url = Column(Text)
    business_category = Column(String(20))
    skill = Column(String(30))
    business_number = Column(String(30))
    venture_registration_number = Column(String(30))
    bond_issue_date = Column(Date)
    main_banner_img_url = Column(Text)


class CompaniesLimitedPartner(Base):
    __tablename__ = 'companies_limited_partners'

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, nullable=False)
    lp_id = Column(Integer, nullable=False)
