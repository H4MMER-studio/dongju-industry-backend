from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr


class Product(Enum, str):
    """
    To Do
    - 제품의 경우 Enum 객체로 저장할 것인지 고민
    """

    pass


class InquiryBase(BaseModel):
    title: str
    email: EmailStr
    person_name: str
    company_name: str
    product: Product
    phone_number: str
    details: str


class CreateInquiry(InquiryBase):
    class Config:
        schema_extra = {"example": {}}


class UpdateInquiry(InquiryBase):
    title: Optional[str]
    email: Optional[EmailStr]
    person_name: Optional[str]
    company_name: Optional[str]
    product: Optional[Product]
    phone_number: Optional[str]
    details: Optional[str]

    class Config:
        schema_extra = {"example": {}}
