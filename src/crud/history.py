from collections import defaultdict

from fastapi import Request

from src.crud.base import CRUDBase
from src.schema import CreateHistory, UpdateHistory


class CRUDHistory(CRUDBase[CreateHistory, UpdateHistory]):
    async def get_multi(
        self,
        request: Request,
        skip: int,
        limit: int,
        sort: list[str],
    ) -> dict:
        result = await super().get_multi(
            request=request, skip=skip, limit=limit, sort=sort
        )
        if result["size"]:
            converted_data: list[dict] = []
            same_year_data: dict[int, list[dict]] = defaultdict(list)
            for document in result["data"]:
                start_year = int(str(document["history_year"])[:3] + "0")
                same_year_data[start_year].append(document)

            for start_year, documents in same_year_data.items():
                converted_data.append(
                    {"start_year": start_year, "data": documents}
                )

            result["data"] = converted_data

        return result


history_crud = CRUDHistory(collection="histories")
