from fastapi import Request
from pymongo import ASCENDING, DESCENDING

from src.crud.base import CRUDBase
from src.schema import CreateInquiry, UpdateInquiry
from src.util import create_decompsed_korean_field, decompose_korean, datetime_to_str


class CRUDIquiry(CRUDBase[CreateInquiry, UpdateInquiry]):
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
            data_size = len(documents)
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
        if result["size"] and not type == "search":
            for data in result["data"]:
                data["inquiry_company_name"] = data.pop(
                    "inquiry_company_name"
                )["composed"]
                data["inquiry_person_name"] = data.pop("inquiry_person_name")[
                    "composed"
                ]

        return result

    async def create(
        self, request: Request, insert_data: CreateInquiry
    ) -> bool:
        converted_insert_data = await create_decompsed_korean_field(
            data=insert_data.dict(),
            fields=["inquiry_person_name", "inquiry_company_name"],
        )

        result = await super().create(
            request=request, insert_data=converted_insert_data
        )
        return result

    async def update(
        self, request: Request, id: str, update_data: UpdateInquiry
    ) -> dict:
        converted_update_data = await create_decompsed_korean_field(
            data=update_data.dict(exclude_none=True),
            fields=["inquiry_person_name", "inquiry_company_name"],
        )
        result = await super().update(
            request=request, id=id, update_data=converted_update_data
        )
        return result


inquiry_crud = CRUDIquiry(collection="inquiries")
