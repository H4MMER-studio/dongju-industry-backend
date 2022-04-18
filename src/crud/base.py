from typing import Generic, TypeVar

from bson.objectid import ObjectId
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from pymongo import ASCENDING, DESCENDING, DeleteOne, UpdateOne

CreateSchema = TypeVar("CreateSchema", bound=BaseModel)
UpdateSchema = TypeVar("UpdateSchema", bound=BaseModel)


class CRUDBase(Generic[CreateSchema, UpdateSchema]):
    def __init__(self, collection: str) -> None:
        self.collection = collection

    async def get_one(self, request: Request, id: str) -> dict | None:
        document = await request.app.db[self.collection].find_one(
            {"_id": ObjectId(id)}
        )
        document["_id"] = str(document["_id"])

        return document

    async def get_multi(
        self,
        request: Request,
        skip: int,
        limit: int,
        sort: list[str],
        filter_field: str | None = None,
        filter_value: str | None = None,
    ) -> dict | None:
        filter = {}
        if filter_value:
            filter[filter_field] = filter_value

        db = request.app.db[self.collection]
        if not (data_size := await db.count_documents(filter)):
            return None
        else:
            result = {"data_size": data_size}
            query = db.find(filter)

        if sort:
            sort_field = []

            for query_string in sort:
                field, option = query_string.split(" ")

                field = field.replace("-", "_")

                if option == "asc":
                    option = ASCENDING
                elif option == "desc":
                    option = DESCENDING
                else:
                    raise ValueError

                sort_field.append((field, option))

            query = query.sort(sort_field)

        documents = (
            await query.skip(skip - 1).limit(limit).to_list(length=None)
        )

        for document in documents:
            document["_id"] = str(document["_id"])

        result["data"] = documents

        return result

    async def create(
        self, request: Request, insert_data: CreateSchema
    ) -> bool:
        inserted_document = await request.app.db[self.collection].insert_one(
            jsonable_encoder(insert_data)
        )

        result = inserted_document.acknowledged

        return result

    async def update(
        self, request: Request, id: str, update_data: UpdateSchema
    ) -> bool:
        update_data = update_data.dict(exclude_none=True)

        updated_document = await request.app.db[
            self.collection
        ].find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": jsonable_encoder(update_data)},
            upsert=False,
        )

        return updated_document

    async def delete(self, request: Request, id: str) -> bool:
        deleted_document = await request.app.db[
            self.collection
        ].find_one_and_delete({"_id": ObjectId(id)})

        return deleted_document

    async def bulk_update(
        self, request: Request, update_data: list[UpdateSchema], model: str
    ) -> bool:
        query: list[UpdateOne] = []

        for data in update_data:
            id = ObjectId(data.dict(exclude_none=True).pop(f"{model}_id"))
            query.append(
                UpdateOne({"_id": id}, {"$set": jsonable_encoder(data)})
            )

        updated_document = await request.app.db[self.collection].bulk_write(
            query
        )

        return (
            True
            if (updated_document.modified_count == len(update_data))
            else False
        )

    async def bulk_delete(self, request: Request, ids: list[str]) -> bool:
        query: list[DeleteOne] = [
            DeleteOne({"_id": ObjectId(id)}) for id in ids
        ]

        deleted_document = await request.app.db[self.collection].bulk_write(
            query
        )

        return True if deleted_document.deleted_count == len(ids) else False
