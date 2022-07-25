from fastapi import Request

from src.crud.base import CRUDBase
from src.schema import CreateCertification, UpdateCertification


class CRUDCertification(CRUDBase[CreateCertification, UpdateCertification]):
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
        return await super().get_multi(
            request=request,
            skip=skip,
            limit=limit,
            sort=sort,
            type=type,
            field=field,
            value=value,
        )


certification_crud = CRUDCertification(collection="certifications")
