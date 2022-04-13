from fastapi import Request
from pymongo import ASCENDING, DESCENDING

from src.crud.base import CRUDBase
from src.schema import CreateHistory, UpdateHistory


class CRUDHistory(CRUDBase[CreateHistory, UpdateHistory]):
    async def get_multi(
        self, request: Request, skip: int, limit: int, sort: list[str]
    ) -> list[dict[str, list[dict]]] | None:
        result: list = []
        temp: dict = {}

        query = request.app.db[self.collection].find()

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

        documents = await query.to_list(length=None)
        documents = documents[skip:limit]

        for document in documents:
            document["_id"] = str(document["_id"])

        for document in documents:
            start_year = str(document["history_year"])[:3] + "0"

            if start_year in temp:
                temp[start_year].append(document)
            else:
                temp[start_year] = [document]

        for start_year, value in temp.items():
            result.append({"start_year": start_year, "value": value})

        return result


history_crud = CRUDHistory(collection="histories")
