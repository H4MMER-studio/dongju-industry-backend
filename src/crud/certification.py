from fastapi import Request

from src.crud.base import CRUDBase
from src.schema import CreateCertification, UpdateCertification
from src.util import datetime_to_str, str_to_datetime


class CRUDCertification(CRUDBase[CreateCertification, UpdateCertification]):
    async def get_one(self, request: Request, id: str) -> dict | None:
        document = await super().get_one(request, id)

        if document["certification_start_date"]:
            document["certification_start_date"] = await datetime_to_str(
                datetime=document["certification_start_date"]
            )

        if document["certification_end_date"]:
            document["certification_end_date"] = await datetime_to_str(
                datetime=document["certification_end_date"]
            )

        return document

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

        if result["size"]:
            for document in result["data"]:
                if document["certification_start_date"]:
                    document[
                        "certification_start_date"
                    ] = await datetime_to_str(
                        datetime=document["certification_start_date"],
                    )

                if document["certification_end_date"]:
                    document["certification_end_date"] = await datetime_to_str(
                        datetime=document["certitication_end_date"],
                    )

        return result

    async def create(
        self, request: Request, insert_data: CreateCertification
    ) -> bool:
        converted_insert_data = insert_data.dict()

        if converted_insert_data["certification_start_date"]:
            converted_insert_data[
                "certification_start_date"
            ] = await str_to_datetime(
                date_string=converted_insert_data["certification_start_date"],
                format="%Y-%m-%d",
            )

        if converted_insert_data["certification_end_date"]:
            converted_insert_data[
                "certification_end_date"
            ] = await str_to_datetime(
                date_string=converted_insert_data["certification_end_date"],
                format="%Y-%m-%d",
            )

        return await super().create(
            request=request, insert_data=converted_insert_data
        )

    async def update(
        self, request: Request, id: str, update_data: UpdateCertification
    ) -> bool:
        if update_data.certification_start_date:
            update_data.certification_start_date = await str_to_datetime(
                date_string=update_data.certification_start_date,
                format="%Y-%m-%d",
            )

        if update_data.certification_end_date:
            update_data.certification_end_date = await str_to_datetime(
                date_string=update_data.certification_end_date,
                format="%Y-%m-%d",
            )

        return await super().update(request, id, update_data)


certification_crud = CRUDCertification(collection="certifications")
