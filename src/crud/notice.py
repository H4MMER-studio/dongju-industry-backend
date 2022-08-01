from bson.objectid import ObjectId
from fastapi import Request
from pymongo import DESCENDING

from src.crud.base import CRUDBase
from src.schema import CreateNotice, UpdateNotice
from src.util import datetime_to_str, file_crud


class CRUDNotice(CRUDBase[CreateNotice, UpdateNotice]):
    async def get_one(self, request: Request, id: str) -> dict:
        session = request.app.db[self.collection]

        document = await session.find_one({"_id": ObjectId(id)})
        document["_id"] = str(document["_id"])
        document["created_at"] = datetime_to_str(
            datetime=document["created_at"]
        )

        if document["updated_at"]:
            document["updated_at"] = datetime_to_str(
                datetime=document["updated_at"]
            )

        result: dict = {"data": {"current": document}}

        latest_documents = await session.find(
            filter={"notice_type": document["notice_type"]},
            sort=[("$natural", DESCENDING)],
            limit=2,
        ).to_list(length=None)

        for latest_document in latest_documents:
            latest_document["_id"] = str(latest_document["_id"])
            latest_document["created_at"] = datetime_to_str(
                datetime=latest_document["created_at"]
            )

            if latest_document["updated_at"]:
                latest_document["updated_at"] = datetime_to_str(
                    datetime=latest_document["updated_at"]
                )

        result["data"]["latest"] = latest_documents
        result["size"] = len(document) + len(latest_documents)

        return result

    async def delete(self, request: Request, id: str) -> dict:
        result: dict = {"status": True, "detail": ""}
        deleted_document = await super().delete(request, id)
        if not deleted_document:
            result["status"] = False
            result["detail"] = "Not Found"

        else:
            for image, file in zip(
                deleted_document["notice_images"],
                deleted_document["notice_files"],
            ):
                if image:
                    image_result = await file_crud.delete(
                        object_key=image["key"]
                    )
                    if (
                        image_result["ResponseMetadata"]["HTTPStatusCode"]
                        != 204
                    ):
                        result["status"] = False
                        result["detail"] = "AWS S3"

                if file:
                    file_result = await file_crud.delete(
                        object_key=image["key"]
                    )
                    if (
                        file_result["ResponseMetadata"]["HTTPStatusCode"]
                        != 204
                    ):
                        result["status"] = False
                        result["detail"] = "AWS S3"

        return result


notice_crud = CRUDNotice(collection="notices")
