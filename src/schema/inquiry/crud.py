from enum import Enum

from pydantic import BaseModel, EmailStr


class ProductType(str, Enum):
    AIR_CONDITIONER = "air-conditioner"
    FREEZE_PROTECTION_DAMPER_COIL = "freeze-protection-damper-coil"
    EXHAUST_UNIT = "exhaust-unit"
    BUBBLE_DAMPER = "bubble-damper"
    FULLY_SEALED_DOOR = "fully-sealed-door"


class InquiryType(str, Enum):
    ESTIMATE = "estimate"
    AS = "after-service"
    ETC = "etc"


class InquiryBase(BaseModel):
    inquiry_type: InquiryType | None
    inquiry_title: str | None
    inquiry_email: EmailStr | None
    inquiry_person_name: str | None
    inquiry_company_name: str | None
    inquiry_product_type: ProductType | None
    inquiry_phone_number: str | None
    inquiry_content: str | None
    inquiry_resolved_status: bool = False


class CreateInquiry(InquiryBase):
    inquiry_type: InquiryType
    inquiry_product_type: ProductType
    inquiry_title: str
    inquiry_email: EmailStr
    inquiry_person_name: str
    inquiry_company_name: str
    inquiry_phone_number: str
    inquiry_content: str

    class Config:
        schema_extra: dict[str, dict] = {
            "example": {
                "inquiry_type": "estimate",
                "inquiry_title": "안녕하세요. 댐퍼 코일 견적 관련 문의입니다.",
                "inquiry_content": "안녕하세요. 저희 회사 실험실에 사용할 예정입니다.",
                "inquiry_person_name": "김해머",
                "inquiry_company_name": "해머스튜디오",
                "inquiry_phone_number": "010-1234-5678",
                "inquiry_email": "H4MMER@naver.com",
                "inquiry_product_type": "freeze-protection-damper-coil",
            }
        }


class UpdateInquiry(InquiryBase):
    class Config:
        schema_extra: dict[str, dict] = {"example": {}}
