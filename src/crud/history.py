from fastapi import Request
from pymongo import ASCENDING, DESCENDING

from src.crud.base import CRUDBase
from src.schema import CreateHistory, UpdateHistory
from src.util import datetime_to_str


class CRUDHistory(CRUDBase[CreateHistory, UpdateHistory]):
    async def get_multi(
        self,
        request: Request,
        sort: list[str],
    ) -> dict | None:
        result: dict = {}
        temp: dict = {}
        data: list = []

        query = request.app.db[self.collection].find()

        if sort:
            sort_field: list = []
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

        if not (data_size := len(documents)):
            return None

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

            start_year = str(document["history_year"])[:3] + "0"
            if start_year in temp:
                temp[start_year].append(document)
            else:
                temp[start_year] = [document]

        for start_year, value in temp.items():
            data.append({"start_year": start_year, "value": value})

        result["size"] = data_size
        result["data"] = data

        return result


history_crud = CRUDHistory(collection="histories")
