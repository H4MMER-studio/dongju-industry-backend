from fastapi import Request

from src.crud.base import CRUDBase
from src.schema import CreateCertification, UpdateCertification


class CRUDCertification(CRUDBase[CreateCertification, UpdateCertification]):
    async def create(
        self, request: Request, insert_data: CreateCertification
    ) -> bool:
        converted_insert_data = insert_data.dict()
        return await super().create(
            request=request, insert_data=converted_insert_data
        )


certification_crud = CRUDCertification(collection="certifications")
