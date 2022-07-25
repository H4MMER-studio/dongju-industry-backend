from typing import Generic, TypeVar

from bson.objectid import ObjectId
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from pymongo import ASCENDING, DESCENDING, DeleteOne, UpdateOne

from src.util import datetime_to_str, decompose_korean, get_datetime

CreateSchema = TypeVar("CreateSchema", bound=BaseModel)
UpdateSchema = TypeVar("UpdateSchema", bound=BaseModel)


class CRUDBase(Generic[CreateSchema, UpdateSchema]):
    def __init__(self, collection: str) -> None:
        self.collection = collection

    async def get_one(self, request: Request, id: str) -> dict | None:
        db = request.app.db[self.collection]
        if not (document := db.find_one({"_id": ObjectId(id)})):
            return None

        else:
            document["_id"] = str(document["_id"])
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
    ) -> dict | None:
        session = request.app.db[self.collection]

        pipeline: dict = {}
        if type == "filter" and field and value:
            pipeline[field] = value

        elif field and value:
            decomposed_keyword: str = await decompose_korean(value)
            converted_field: str = field.replace("-", "_")

            pipeline[f"{converted_field}.decomposed"] = {
                "$regex": f".*{decomposed_keyword}.*",
                "$options": "i",
            }

        sort_field: list = []
        if sort:
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

        else:
            sort_field.append(("$natural", DESCENDING))

        if skip:
            skip -= 1

        documents = await session.find(
            filter=pipeline,
            sort=sort_field,
            skip=skip,
            limit=limit - skip,
        ).to_list(length=None)

        if type == "search":
            documents = [
                {converted_field: document[converted_field]["composed"]}
                for document in documents
            ]

        else:
            print(documents)
            for document in documents:
                document["_id"] = str(document["_id"])

                document["created_at"] = await datetime_to_str(
                    datetime=document["created_at"]
                )

                if document["updated_at"]:
                    document["updated_at"] = await datetime_to_str(
                        datetime=document["updated_at"]
                    )

                if document["deleted_at"]:
                    document["deleted_at"] = await datetime_to_str(
                        datetime=document["deleted_at"]
                    )

        result: dict = {"size": len(documents), "data": documents}

        return result

    async def create(
        self, request: Request, insert_data: CreateSchema
    ) -> bool:
        insert_data = insert_data.dict()
        insert_data["created_at"] = get_datetime()

        inserted_document = await request.app.db[self.collection].insert_one(
            jsonable_encoder(insert_data)
        )

        result = inserted_document.acknowledged

        return result

    async def update(
        self, request: Request, id: str, update_data: UpdateSchema
    ) -> bool:
        update_data = update_data.dict(exclude_none=True)
        update_data["updated_at"] = get_datetime()

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
