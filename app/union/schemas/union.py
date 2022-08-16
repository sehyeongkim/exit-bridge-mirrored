import datetime as dt

from typing import Optional, List
from enum import Enum
from pydantic import BaseModel, Field


class UnionStatus(Enum):
    RECRUITING = '결성진행중'
    OPERATING = '운용중'
    DISMISSED = '해산'


class UnionRegistrationRequestSchema(BaseModel):
    union_name: str = Field(..., description='조합명')
    unit_share_price: int = Field(..., description='1좌당 금액')
    total_share_number: int = Field(..., description='총 출자좌수')
    total_share_price: int = Field(..., description='총 출자금액')
    establishment_date: dt.datetime = Field(..., description='결성일자')
    expire_date: dt.datetime = Field(..., description='만기일자')
    status: Optional[UnionStatus] = Field(UnionStatus.RECRUITING.value, description='모집상태: 결성진행중|운용중|해산')

    class Config:
        orm_mode = True
        use_enum_values = True


class UnionHistoricalStatus(BaseModel):
    before_operation: int
    in_operation: int
    dismissal: int


class Union(BaseModel):
    union_id: int
    gp_id: int
    company_id: int
    company_name: str
    union_name: str
    establishment_date: str
    expire_date: str
    confirmation_status: str
    total_lp_number: int
    total_share_price: int


class UnionSummary(BaseModel):
    AUM: int
    total_company_number: int
    total_union_number: int
    total_lp_number: int


class UnionOverallResponseSchema(BaseModel):
    union_historial_status: UnionHistoricalStatus
    unions: List[Union]
    union_summary: UnionSummary