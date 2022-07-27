from fastapi import Request

from src.crud.base import CRUDBase
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
    ) -> dict | None:
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
                data["inquiry_person_name"] = data.pop("delivery_product")[
                    "composed"
                ]

        return result

    async def create(
        self, request: Request, insert_data: CreateDelivery
    ) -> bool:
        insert_data = await create_decompsed_korean_field(
            schema=insert_data,
            fields=["delivery_supplier", "delivery_product"],
        )

        result = await super().create(request=request, insert_data=insert_data)
        return result


delivery_crud = CRUDDelivery(collection="deliveries")
