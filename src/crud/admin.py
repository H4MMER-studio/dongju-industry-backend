from fastapi import Request
from passlib.context import CryptContext

from src.crud.base import CRUDBase
from src.schema import CreateAdmin, UpdateAdmin


class CRUDAdmin(CRUDBase[CreateAdmin, UpdateAdmin]):
    async def get_one(
        self, request: Request, user_data: CreateAdmin
    ) -> dict | None:

        return None

    async def create(self, request: Request, insert_data: CreateAdmin) -> bool:
        password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        insert_data.admin_password = password_context.hash(
            insert_data.admin_password
        )

        print(insert_data)
        return False


admin_crud = CRUDAdmin(collection="admin")
