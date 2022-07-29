from fastapi import Request

from src.crud.base import CreateSchema, CRUDBase
from src.schema import CreateDelivery, UpdateDelivery
from src.util import create_decompsed_korean_field


class CRUDDelivery(CRUDBase[CreateDelivery, UpdateDelivery]):
    async def get_multi(
        self,
        request: Request,
        skip: int,
        limit: int,
        sort: list[str],
        type: str | None,
        field: str | None,
        value: str | None,
    ) -> dict:
        result = await super().get_multi(
            request=request,
            skip=skip,
            limit=limit,
            sort=sort,
            type=type,
            field=field,
            value=value,
        )
        if result["size"] and not type == "search":
            for data in result["data"]:
                data["delivery_supplier"] = data.pop("delivery_supplier")[
                    "composed"
                ]
                data["delivery_product"] = data.pop("delivery_product")[
                    "composed"
                ]

        return result

    async def create(
        self, request: Request, insert_data: CreateSchema
    ) -> bool:
        converted_insert_data = await create_decompsed_korean_field(
            data=insert_data.dict(),
            fields=["delivery_supplier", "delivery_product"],
        )

        result = await super().create(
            request=request, insert_data=converted_insert_data
        )
        return result

    async def update(
        self, request: Request, id: str, update_data: UpdateDelivery
    ) -> dict:
        converted_update_data = await create_decompsed_korean_field(
            data=update_data.dict(exclude_none=True),
            fields=["delivery_supplier", "delivery_product"],
        )
        result = await super().update(
            request=request, id=id, update_data=converted_update_data
        )
        return result


delivery_crud = CRUDDelivery(collection="deliveries")
