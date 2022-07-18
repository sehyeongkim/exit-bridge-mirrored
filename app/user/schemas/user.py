import datetime

from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, List


class GetUserListResponseSchema(BaseModel):
    id: int = Field(..., description="ID")
    email: str = Field(..., description="Email")
    nickname: str = Field(..., description="Nickname")

    class Config:
        orm_mode = True


class UserLoginRequestSchema(BaseModel):
    kakao_access_token: str = Field(..., description='Kakao Access Token')
    phone_number: Optional[str] = Field(..., description='휴대폰번호')
    name: Optional[str] = Field(..., description='유저 실명')


class UserLoginResponseSchema(BaseModel):
    user_id: str = Field(..., description='User ID')
    kakao_user_id: str = Field(..., description='Kakao User ID')
    access_token: str = Field(..., description='User Access Token')

    class Config:
        orm_mode = True


class GPWorkExperience(BaseModel):
    career_start_date: datetime = Field(..., description='경력시작일')
    career_end_date: datetime = Field(None, description='경력종료일')
    worked_company: str = Field(..., description='회사')
    worked_position_description: str = Field(..., description='직책')


class UnionEstablishmentExperience(BaseModel):
    union_start_date: datetime = Field(..., description='조합 설립일')
    union_end_date: datetime = Field(..., description='조합 해산일')
    union_id_certificate_url: str = Field(..., description='조합 고유번호 증서')
    union_investment_certificate_url: str = Field(..., description='조합 투자증서')


class GPApplicationRequestSchema(BaseModel):
    name: str = Field(..., description='GP name')
    phone_number: str = Field(..., description='Phone Number')
    registration_number: str = Field(..., description='주민등록번호')
    zip_code: str = Field(..., description='우편번호')
    road_name_address: str = Field(..., description='도로명주소')
    detailed_address: str = Field(None, description='상세주소')
    work_experience: List[GPWorkExperience] = Field(None, description='경력 리스트')
    nickname: str = Field(..., description='닉네임')
    year_of_gp_experience: int = Field(..., description='경력 년도')
    gp_union_establishment_experience: List[UnionEstablishmentExperience] = Field(None, description='조합 설립경험')


class ArticleJson(BaseModel):
    title: str = Field(None, description='기사 제목')
    url: str = Field(None, description='기사 url')
    issue_date: datetime = Field(None, description='기사 발행일')
    tags: List[str] = Field(None, description='기사 태그')
    thumbnail_urls: List[str] = Field(None, description='썸네일 이미지 url')


class RecruitmentStatus(Enum):
    open: str = '모집중'
    closed: str = '모집마감'


class CompanyRegistrationRequestSchema(BaseModel):
    gp_id: int = Field(...)
    company_name: str = Field(...)
    logo_img_url: str = Field(..., description='회사 로고 이미지 url')
    main_banner_img_url: str = Field(..., description='메인 배너 이미지 url')
    product_name: str = Field(None, description='프로덕트 이름')
    investment_stage: str = Field(None, description='투자 단계')
    investment_method: str = Field(None, description='투자 방법')
    total_capital: str = Field(None, description='총 자본금')
    total_investment: str = Field(None, description='총 투자금')
    company_classification: str = Field(None, description='회사 분류')
    corporate_classification: str = Field(None, description='법인 분류')
    establishment_date: datetime = Field(..., description='회사 설립일')
    homepage_url: str = Field(None, description='홈페이지 url')
    business_category: str = Field(None, description='사업 분류')
    skill: str = Field(None, description='기업 기술')
    business_number: str = Field(..., description='사업자등록번호')
    venture_registration_number: str = Field(None, description='벤처등록번호')
    bond_issue_date: str = Field(None, description='사채발행일자')
    main_post_title: str = Field(..., description='메인 포스트')
    main_post_intro: str = Field(..., description='메인 포스트 간단소개글')
    main_post_html_text: str = Field(..., description='위지위그 편집기 텍스트')
    attachment_json: List[str] = Field(None, description='첨부파일 json')
    article_json: ArticleJson = Field(None, description='관련기사 json')
    recruitment_status: RecruitmentStatus = Field(..., description='모집상태: 모집중|모집마감')
    is_open_to_public: bool = Field(..., description='공개여부: 공개|비공개')


class UnionRegistrationRequestSchema(BaseModel):
    union_name: str = Field(..., description='조합명')
    gp_id: int = Field(..., description='GP ID')
    company_id: int = Field(..., description='Company ID')
    unit_share_price: int = Field(..., description='1좌당 금액')
    total_share_number: int = Field(..., description='총 출자좌수')
    total_share_price: int = Field(..., description='총 출자금액')
    establishment_date: datetime = Field(..., description='결성일자')
    expire_date: datetime = Field(..., description='만기일자')


class LPApplicationManagementRequestSchema(BaseModel):
    lp_application_form_id: int = Field(..., description='LP Application Form ID')
    gp_id: int = Field(..., description='GP ID')
    union_id: int = Field(..., description='Union ID')
    is_approved: bool = Field(..., description='승인여부: 승인|미승인')
    reject_reason: str = Field(None, description='반려사유')
