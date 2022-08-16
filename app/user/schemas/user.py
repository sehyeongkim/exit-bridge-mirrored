import datetime as dt

from enum import Enum
from fastapi import Form, UploadFile, File
from pydantic import BaseModel, Field
from typing import Optional, List


class UserType(Enum):
    USER = 'user'
    LP = 'lp'
    GP = 'gp'
    ADMIN = 'admin'


class GetUserListResponseSchema(BaseModel):
    id: int = Field(..., description="ID")
    email: str = Field(..., description="Email")
    nickname: str = Field(..., description="Nickname")

    class Config:
        orm_mode = True


class UserLoginRequestSchema(BaseModel):
    kakao_access_token: str = Field(..., description='Kakao Access Token')
    phone_number: Optional[str] = Field(description='휴대폰번호')
    email: Optional[str] = Field(description='이메일')

    class Config:
        orm_mode = True


class UserLoginResponseSchema(BaseModel):
    user_id: str = Field(..., description='User ID')
    kakao_user_id: str = Field(..., description='Kakao User ID')
    access_token: str = Field(..., description='User Access Token')


class GPCareer(BaseModel):
    career_start_date: dt.datetime = Field(..., description='경력시작일')
    career_end_date: Optional[dt.datetime] = Field(description='경력종료일')
    worked_company: str = Field(..., description='회사')
    worked_position_description: str = Field(..., description='직책')

    class Config:
        orm_mode = True


class UnionEstablishmentExperience(BaseModel):
    union_start_date: dt.datetime = Field(..., description='조합 설립일')
    union_end_date: dt.datetime = Field(..., description='조합 해산일')
    union_id_certificate_url: str = Field(..., description='조합 고유번호 증서')
    union_investment_certificate_url: str = Field(..., description='조합 투자증서')

    class Config:
        orm_mode = True


class GPApplicationRequestSchema(BaseModel):
    name: str = Field(..., description='GP 실명')
    registration_number: str = Field(..., description='주민등록번호')
    zip_code: str = Field(..., description='우편번호')
    road_name_address: str = Field(..., description='도로명주소')
    detailed_address: str = Field(..., description='상세주소')
    careers: Optional[List[GPCareer]] = Field(description='경력 리스트')
    nickname: str = Field(..., description='닉네임')
    year_of_gp_experience: int = Field(0, description='GP 운용 경력 년수')
    union_establishment_experiences: Optional[List[UnionEstablishmentExperience]] = Field(description='조합 설립경험')
    applied_date: dt.datetime = Field(dt.datetime.now().date(), description='GP 신청일자')

    class Config:
        orm_mode = True


class LPApplicationManagementRequestSchema(BaseModel):
    lp_application_form_id: int = Field(..., description='LP Application Form ID')
    gp_id: int = Field(..., description='GP ID')
    union_id: int = Field(..., description='Union ID')
    is_approved: bool = Field(..., description='승인여부: 승인|미승인')
    reject_reason: Optional[str] = Field(description='반려사유')

    class Config:
        orm_mode = True


class S3UploadRequestSchema(BaseModel):
    file_path: str = Form(..., description="s3 bucket file path")
    file: UploadFile = File(..., description="file")

    class Config:
        orm_mode = True