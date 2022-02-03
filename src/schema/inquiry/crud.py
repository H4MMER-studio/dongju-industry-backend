from enum import Enum

from pydantic import BaseModel, EmailStr


class Product(Enum, str):
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
    class Config:
        schema_extra = {"example": {}}
