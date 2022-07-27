from datetime import datetime

from fastapi import Header, HTTPException, Request, status
from jose import JWTError, jwt
from passlib.context import CryptContext

from src.core import get_settings
from src.crud.base import CRUDBase
from src.schema import CreateAdmin, UpdateAdmin


class CRUDAdmin(CRUDBase[CreateAdmin, UpdateAdmin]):
    async def auth_user(
        self, request: Request, access_token=Header(...)
    ) -> bool:
        """
        에러 핸들링 필요
        """
        try:
            payload = jwt.decode(
                token=access_token,
                key=get_settings().SECRET_KEY,
                algorithms=[get_settings().ALGORITHM],
            )
            admin_id = payload.get("sub")
            if not admin_id:
                raise HTTPException(
                    detail="access token doesn't exist",
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

            elif not request.app.db[self.collection].find_one(
                {"admin_id": admin_id}
            ):
                raise HTTPException(
                    detail="not found",
                    status_code=status.HTTP_404_NOT_FOUND,
                )

            else:
                return True

        except JWTError as jwt_error:
            raise HTTPException(
                detail=str(jwt_error),
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

    async def get_one(
        self, request: Request, user_data: CreateAdmin
    ) -> dict | None:
        password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        user = await request.app.db[self.collection].find_one(
            {"admin_id": user_data.admin_id}
        )

        if not user:
            return None

        elif not password_context.verify(
            secret=user_data.admin_password, hash=user["admin_password"]
        ):
            raise

        else:
            encoded_data = {
                "sub": user["admin_id"],
                "exp": datetime(year=2099, month=12, day=31),
            }
            access_token = jwt.encode(
                claims=encoded_data,
                key=get_settings().SECRET_KEY,
                algorithm=get_settings().ALGORITHM,
            )
            return access_token

    async def create(self, request: Request, insert_data: CreateAdmin) -> bool:
        password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        insert_data.admin_password = password_context.hash(
            secret=insert_data.admin_password
        )

        result = await super().create(request=request, insert_data=insert_data)
        return result


admin_crud = CRUDAdmin(collection="admin")
