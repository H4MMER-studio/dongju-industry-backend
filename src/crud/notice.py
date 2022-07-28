from bson.objectid import ObjectId
from fastapi import Request
from pymongo import DESCENDING

from src.crud.base import CRUDBase
from src.schema import CreateNotice, UpdateNotice


class CRUDNotice(CRUDBase[CreateNotice, UpdateNotice]):
    async def get_one(self, request: Request, id: str) -> dict:
        session = request.app.db[self.collection]

        document = await session.find_one({"_id": ObjectId(id)})
        document["_id"] = str(document["_id"])
        result: dict = {"data": {"current": document}}

        latest_documents = await session.find(
            filter={"notice_type": document["notice_type"]},
            sort=[("$natural", DESCENDING)],
            limit=2,
        ).to_list(length=None)

        for latest_document in latest_documents:
            latest_document["_id"] = str(latest_document["_id"])

        result["data"]["latest"] = latest_documents
        result["size"] = len(document) + len(latest_documents)

        return result


notice_crud = CRUDNotice(collection="notices")
