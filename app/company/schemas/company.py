import datetime as dt

from enum import Enum
from pydantic import BaseModel, Field, validator
from typing import Optional, List


class ArticleJson(BaseModel):
    title: str = Field(..., description='기사 제목')
    url: str = Field(..., description='기사 url')
    issue_date: dt.datetime = Field(..., description='기사 발행일')
    tags: Optional[List[str]] = Field(description='기사 태그')
    thumbnail_urls: Optional[List[str]] = Field(description='썸네일 이미지 url')

    @validator('issue_date')
    def to_str(cls, v):
        return dt.datetime.strftime(v, '%Y-%m-%d %H:%M')


class RecruitmentStatus(Enum):
    OPEN = '모집중'
    CLOSED = '모집마감'


class CompanyRegistrationRequestSchema(BaseModel):
    company_name: str = Field(...)
    union_id: int = Field(..., description='회사에 연결되는 투자조합 ID')
    logo_img_url: str = Field(..., description='회사 로고 이미지 url')
    main_banner_img_url: str = Field(..., description='메인 배너 이미지 url')
    product_name: str = Field(..., description='프로덕트 이름')
    investment_stage: Optional[str] = Field(description='투자 단계')
    investment_method: Optional[str] = Field(description='투자 방법')
    total_capital: Optional[float] = Field(description='총 자본금')
    total_investment: Optional[float] = Field(description='총 투자금')
    company_classification: Optional[str] = Field(description='회사 분류')
    corporate_classification: Optional[str] = Field(None, description='법인 분류')
    establishment_date: dt.datetime = Field(..., description='회사 설립일')
    homepage_url: Optional[str] = Field(description='홈페이지 url')
    business_category: Optional[str] = Field(description='사업 분류')
    skill: Optional[str] = Field(description='기업 기술')
    business_number: str = Field(..., description='사업자등록번호')
    venture_registration_number: Optional[str] = Field(description='벤처등록번호')
    bond_issue_date: Optional[dt.datetime] = Field(description='사채발행일자')
    main_post_title: str = Field(..., description='메인 포스트')
    main_post_intro: str = Field(..., description='메인 포스트 간단소개글')
    main_post_html_text: str = Field(..., description='위지위그 편집기 텍스트')
    attachment_json: Optional[List[str]] = Field(description='첨부파일 json')
    article_json: Optional[ArticleJson] = Field(description='관련기사 json')
    recruitment_start_date: Optional[dt.datetime] = Field(None, description='모집시작일')
    recruitment_status: Optional[RecruitmentStatus] = Field(RecruitmentStatus.OPEN.value, description='모집상태: 모집중|모집마감')
    is_open_to_public: bool = Field(..., description='공개여부: 공개|비공개')

    class Config:
        orm_mode = True
        use_enum_values = True
