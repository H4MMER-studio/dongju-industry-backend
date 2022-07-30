from fastapi import Request

from src.crud.base import CreateSchema, CRUDBase
from src.schema import CreateDelivery, UpdateDelivery
from src.util import create_decompsed_korean_field, parse_excel_file


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
        converted_data: list[dict] = []
        if result["size"] and not type == "search":
            for data in result["data"]:
                temp: dict = {}
                temp_date: list = []
                for data_key, data_value in data.items():
                    if data_key == "delivery_supplier":
                        temp["delivery_supplier"] = data_value["composed"]

                    elif data_key == "delivery_product":
                        temp["delivery_product"] = data_value["composed"]

                    elif data_key == "delivery_year":
                        temp_date.append(str(data_value))

                    elif data_key == "delivery_month":
                        if data_value:
                            temp_date.append(str(data_value))

                    else:
                        temp[data_key] = data_value

                temp["delivery_date"] = "-".join(
                    sorted(temp_date, key=lambda x: len(x), reverse=True)
                )

                converted_data.append(temp)

            result["data"] = converted_data

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

    async def bulk_create(
        self, request: Request, insert_data: list[CreateSchema | dict]
    ) -> bool:
        converted_insert_data: list[dict] = []
        excel_data = await parse_excel_file(excel_file=insert_data)
        for data in excel_data:
            converted_data = await create_decompsed_korean_field(
                data=data,
                fields=["delivery_supplier", "delivery_product"],
            )
            converted_insert_data.append(converted_data)

        return await super().bulk_create(
            request=request, insert_data=converted_insert_data
        )

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
