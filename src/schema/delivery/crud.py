from pydantic import validator

from src.schema.crud_base import BaseSchema


class DeliveryBase(BaseSchema):
    """
    납품실적 기본 스키마
    """

    delivery_supplier: str | None
    delivery_product: str | None
    delivery_amount: int | None
    delivery_year: int | None
    delivery_month: int | None
    delivery_reference: str | None


class CreateDelivery(DeliveryBase):
    """
    납품실적 생성 스키마
    """

    delivery_supplier: str
    delivery_product: str
    delivery_amount: int
    delivery_year: int

    @validator("delivery_month")
    def validate_month(cls, value) -> int:
        if value < 1 or value > 12:
            raise ValueError("delivery_month must be between 1 and 12")

        return value

    class Config:
        schema_extra: dict[str, dict] = {
            "example": {
                "delivery_supplier": "(주)세진에스.이",
                "delivery_product": "COOK FAN",
                "delivery_amount": 3,
                "delivery_year": 2012,
                "delivery_month": 2,
                "delivery_reference": "연세대학교",
            },
        }


class UpdateDelivery(DeliveryBase):
    """
    납품실적 수정 스키마
    """

    class Config:
        schema_extra: dict[str, dict] = {
            "example": {"delivery_product": "수정하려는 납품실적 제품"}
        }
