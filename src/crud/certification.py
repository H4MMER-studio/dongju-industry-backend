from fastapi import Request

from src.crud.base import CRUDBase
from src.schema import CreateCertification, UpdateCertification
from src.util import datetime_to_str, file_crud


class CRUDCertification(CRUDBase[CreateCertification, UpdateCertification]):
    async def get_one(self, request: Request, id: str) -> dict | None:
        document = await super().get_one(request=request, id=id)
        if document:
            if document["certification_start_date"]:
                document["certification_start_date"] = datetime_to_str(
                    datetime=document["certification_start_date"]
                )

            if document["certification_end_date"]:
                document["certification_end_date"] = datetime_to_str(
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
                    document["certification_start_date"] = datetime_to_str(
                        datetime=document["certification_start_date"],
                    )

                if document["certification_end_date"]:
                    document["certification_end_date"] = datetime_to_str(
                        datetime=document["certification_end_date"],
                    )

        return result

    async def delete(self, request: Request, id: str) -> dict:
        result: dict = {"status": True, "detail": ""}
        deleted_document = await super().delete(request, id)
        if not deleted_document:
            result["status"] = False
            result["detail"] = "Not Found"

        else:
            for image in deleted_document["certification_images"]:
                response = await file_crud.delete(object_key=image["key"])
                if response["ResponseMetadata"]["HTTPStatusCode"] != 204:
                    result["status"] = False
                    result["detail"] = "AWS S3"

        return result


certification_crud = CRUDCertification(collection="certifications")
