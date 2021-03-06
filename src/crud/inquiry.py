from fastapi import Request

from src.crud.base import CRUDBase
from src.schema import CreateInquiry, UpdateInquiry
from src.util import create_decompsed_korean_field


class CRUDIquiry(CRUDBase[CreateInquiry, UpdateInquiry]):
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
                data["inquiry_company_name"] = data.pop(
                    "inquiry_company_name"
                )["composed"]
                data["inquiry_person_name"] = data.pop("inquiry_person_name")[
                    "composed"
                ]

        return result

    async def create(
        self, request: Request, insert_data: CreateInquiry
    ) -> bool:
        converted_insert_data = await create_decompsed_korean_field(
            schema=insert_data.dict(),
            fields=["inquiry_person_name", "inquiry_company_name"],
        )

        result = await super().create(
            request=request, insert_data=converted_insert_data
        )
        return result

    async def update(
        self, request: Request, id: str, update_data: UpdateInquiry
    ) -> dict:
        converted_update_data = await create_decompsed_korean_field(
            schema=update_data.dict(exclude_none=True),
            fields=["inquiry_person_name", "inquiry_company_name"],
        )
        result = await super().update(
            request=request, id=id, update_data=converted_update_data
        )
        return result


inquiry_crud = CRUDIquiry(collection="inquiries")
