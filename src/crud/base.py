import re
from typing import Generic, TypeVar

from bson.objectid import ObjectId
from fastapi import Request
from pydantic import BaseModel
from pymongo import ASCENDING, DESCENDING, DeleteOne, InsertOne, UpdateOne

from src.util import datetime_to_str, decompose_korean, get_datetime

CreateSchema = TypeVar("CreateSchema", bound=BaseModel)
UpdateSchema = TypeVar("UpdateSchema", bound=BaseModel)


class CRUDBase(Generic[CreateSchema, UpdateSchema]):
    def __init__(self, collection: str) -> None:
        self.collection = collection

    async def get_one(self, request: Request, id: str) -> dict | None:
        session = request.app.db[self.collection]

        result = {"size": 0, "data": {}}

        if document := await session.find_one({"_id": ObjectId(id)}):
            document["_id"] = str(document["_id"])
            document["created_at"] = datetime_to_str(
                datetime=document["created_at"]
            )

            if document["updated_at"]:
                document["updated_at"] = datetime_to_str(
                    datetime=document["updated_at"]
                )

            if document["deleted_at"]:
                document["deleted_at"] = datetime_to_str(
                    datetime=document["deleted_at"]
                )

            result["size"] = 1
            result["data"] = document

        return result

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
        session = request.app.db[self.collection]

        pipeline: dict = {}
        if type == "filter" and field:
            pipeline[field] = value

        elif type == "search" and field:
            if not value:
                return {"size": 0, "data": []}
            decomposed_keyword: str = await decompose_korean(value)
            converted_field: str = field.replace("-", "_")

            pipeline[f"{converted_field}.decomposed"] = {
                "$regex": f".*{decomposed_keyword}.*",
                "$options": "i",
            }

        sort_fields: list = []
        if sort:
            for query_string in sort:
                sort_field, option = query_string.split(" ")
                converted_sort_field = sort_field.replace("-", "_")

                if option == "asc":
                    option = ASCENDING
                elif option == "desc":
                    option = DESCENDING
                else:
                    raise ValueError

                sort_fields.append((converted_sort_field, option))

        else:
            sort_fields.append(("$natural", DESCENDING))

        documents = await session.find(
            filter=pipeline, sort=sort_fields
        ).to_list(length=None)

        if type == "search":
            documents = list(
                {
                    document[converted_field]["composed"]
                    for document in documents
                }
            )
            data_size = len(documents)

        else:
            if (data_size := len(documents)) > 0:
                if skip:
                    skip -= 1
                    documents = documents[skip:limit]
                for document in documents:
                    document["_id"] = str(document["_id"])

                    document["created_at"] = datetime_to_str(
                        datetime=document["created_at"]
                    )

                    if document["updated_at"]:
                        document["updated_at"] = datetime_to_str(
                            datetime=document["updated_at"]
                        )

                    if document["deleted_at"]:
                        document["deleted_at"] = datetime_to_str(
                            datetime=document["deleted_at"]
                        )

        result: dict = {"size": data_size, "data": documents}

        return result

    async def create(
        self, request: Request, insert_data: CreateSchema | dict
    ) -> bool:
        if type(insert_data) is dict:
            converted_insert_data = insert_data.copy()

        else:
            converted_insert_data = insert_data.dict()  # type: ignore

        converted_insert_data["created_at"] = get_datetime()

        inserted_document = await request.app.db[self.collection].insert_one(
            converted_insert_data
        )

        result = inserted_document.acknowledged

        return result

    async def update(
        self, request: Request, id: str, update_data: UpdateSchema | dict
    ) -> dict:
        if type(update_data) is dict:
            converted_update_data = update_data.copy()

        else:
            converted_update_data = update_data.dict(  # type: ignore
                exclude_none=True
            )

        converted_update_data["updated_at"] = get_datetime()

        updated_document = await request.app.db[
            self.collection
        ].find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": converted_update_data},
            upsert=False,
        )

        return updated_document

    async def delete(self, request: Request, id: str) -> dict:
        deleted_document = await request.app.db[
            self.collection
        ].find_one_and_delete({"_id": ObjectId(id)})

        return deleted_document

    async def bulk_create(
        self, request: Request, insert_data: list[CreateSchema | dict]
    ) -> bool:
        query: list[InsertOne] = []
        for data in insert_data:
            if type(data) is dict:
                converted_insert_data = data.copy()

            else:
                converted_insert_data = data.dict()  # type: ignore

            converted_insert_data["created_at"] = get_datetime()
            query.append(InsertOne(converted_insert_data))

        inserted_document = await request.app.db[self.collection].bulk_write(
            query
        )
        return (
            True
            if (inserted_document.inserted_count == len(insert_data))
            else False
        )

    async def bulk_update(
        self, request: Request, update_data: list[UpdateSchema]
    ) -> bool:
        query: list[UpdateOne] = []

        for data in update_data:
            converted_data = data.dict(exclude_none=True)
            for key in converted_data.keys():
                if regex_object := re.match(r"[a-z]+\_id", key):
                    object_id = converted_data[regex_object.group()]

            if regex_object:
                converted_data.pop(regex_object.group())

            converted_data["updated_at"] = get_datetime()

            query.append(
                UpdateOne(
                    {"_id": ObjectId(object_id)}, {"$set": converted_data}
                )
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
