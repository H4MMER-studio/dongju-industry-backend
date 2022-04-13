from src.schema.crud import CreateSchemaBase, CRUDSchemaBase, UpdateSchemaBase


class DeliveryBase(CRUDSchemaBase):
    delivery_supplier: str | None
    delivery_product: str | None
    delivery_amount: int | None
    delivery_year: int | None
    delivery_month: int | None
    delivery_reference: str | None


class CreateDelivery(CreateSchemaBase, DeliveryBase):
    delivery_supplier: str
    delivery_product: str
    delivery_amount: int
    delivery_year: int

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


class UpdateDelivery(UpdateSchemaBase, DeliveryBase):
    class Config:
        schema_extra: dict[str, dict] = {"example": {}}
