from fastapi import Request
from pymongo import ASCENDING, DESCENDING

from src.crud.base import CRUDBase


class CRUDSearch(CRUDBase):
    async def get(
        self,
        request: Request,
        search_field: str,
        search_value: str,
        skip: int,
        limit: int,
        sort: list[str],
    ) -> dict | None:
        db = request.app.db[self.collection]
        search_field = search_field.replace("-", "_")

        if not (data_size := await db.count_documents({})):
            return None

        else:
            result = {"data_size": data_size}

        sort_field = {"score": DESCENDING}

        if self.collection == "inquiry":
            sort_field["inquiry_resolved_status"] = ASCENDING

        for query_string in sort:
            field, option = query_string.split(" ")
            field = field.replace("-", "_")

            if option == "asc":
                option = ASCENDING
            elif option == "desc":
                option = DESCENDING
            else:
                raise ValueError

            sort_field[field] = option

        query: list[dict] = [
            {
                "$search": {
                    "index": self.collection,
                    "autocomplete": {
                        "path": search_field,
                        "query": search_value,
                    },
                },
            },
            {"$sort": sort_field},
        ]

        if skip and limit:
            query.append({"$skip": skip - 1})
            query.append({"$limit": limit - (skip - 1)})

        documents = await db.aggregate(query).to_list(length=None)

        for document in documents:
            document["_id"] = str(document["_id"])

        result["data"] = documents

        return result
