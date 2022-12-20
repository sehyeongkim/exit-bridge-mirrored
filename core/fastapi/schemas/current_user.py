from pydantic import BaseModel, Field
from typing import Optional


class CurrentUser(BaseModel):
    id: Optional[str] = Field(None, description="ID")

    class Config:
        validate_assignment = True
