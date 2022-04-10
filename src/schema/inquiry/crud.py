from enum import Enum

from pydantic import EmailStr

from src.schema.crud import CreateSchemaBase, CRUDSchemaBase, UpdateSchemaBase


class Product(Enum):
    """
    To Do
    - 제품의 경우 Enum 객체로 저장할 것인지 고민
    """

    pass


class InquiryBase(CRUDSchemaBase):
    inquiry_title: str | None
    inquiry_email: EmailStr | None
    inquiry_person_name: str | None
    inquiry_company_name: str | None
    inquiry_product: Product | None
    inquiry_phone_number: str | None
    inquiry_details: str | None
    inquiry_status: bool = False


class CreateInquiry(InquiryBase, CreateSchemaBase):
    inquiry_title: str
    inquiry_email: EmailStr
    inquiry_person_name: str
    inquiry_company_name: str
    inquiry_product: Product
    inquiry_phone_number: str
    inquiry_details: str

    class Config:
        schema_extra: dict[str, dict] = {"example": {}}


class UpdateInquiry(InquiryBase, UpdateSchemaBase):
    class Config:
        schema_extra: dict[str, dict] = {"example": {}}
