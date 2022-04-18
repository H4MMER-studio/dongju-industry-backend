from bson.objectid import ObjectId
from fastapi import Request
from pymongo import DESCENDING

from src.crud.base import CRUDBase
from src.schema import CreateNotice, UpdateNotice


class CRUDNotice(CRUDBase[CreateNotice, UpdateNotice]):
    async def get_one(self, request: Request, id: str) -> dict | None:
        db = request.app.db[self.collection]

        if not (document := await db.find_one({"_id": ObjectId(id)})):
            return None

        else:
            document["_id"] = str(document["_id"])
            result = {"data": document}

            latest_documents = (
                await db.find({"notice_type": document["notice_type"]})
                .sort([("$natural", DESCENDING)])
                .limit(2)
                .to_list(length=None)
            )

            for data in latest_documents:
                data["_id"] = str(data["_id"])
            result["latest_data"] = latest_documents

            return result


notice_crud = CRUDNotice(collection="notices")
