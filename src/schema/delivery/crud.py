from src.schema.crud import CreateSchemaBase, CRUDSchemaBase, UpdateSchemaBase


class DeliveryBase(CRUDSchemaBase):
    delivery_supplier: str | None
    delivery_product: str | None
    delivery_amount: int | None
    delivery_year: int | None
    delivery_month: int | None
    delivery_reference: str | None


class CreateDelivery(DeliveryBase, CreateSchemaBase):
    delivery_supplier: str
    delivery_product: str
    delivery_amount: int
    delivery_year: int

    class Config:
        schema_extra: dict[str, dict] = {"example": {}}


class UpdateDelivery(DeliveryBase, UpdateSchemaBase):
    class Config:
        schema_extra: dict[str, dict] = {"example": {}}
