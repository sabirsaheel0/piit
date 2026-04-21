from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class OperatorBase(BaseModel):
    full_name: str = Field(min_length=2, max_length=255)
    email: EmailStr
    role: str | None = Field(default=None, max_length=100)
    status: str = Field(pattern="^(Active|Inactive)$")


class OperatorCreate(OperatorBase):
    password: str = Field(min_length=8, max_length=128)


class OperatorUpdate(BaseModel):
    full_name: str = Field(min_length=2, max_length=255)
    email: EmailStr
    status: str = Field(pattern="^(Active|Inactive)$")
    password: str | None = Field(default=None, min_length=8, max_length=128)


class OperatorOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    email: EmailStr
    role: str | None
    status: str
    is_master: bool
    created_at: datetime
    updated_at: datetime


class OperatorListResponse(BaseModel):
    items: list[OperatorOut]
    total: int
    page: int
    page_size: int
