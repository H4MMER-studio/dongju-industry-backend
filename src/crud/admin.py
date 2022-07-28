from datetime import datetime

from fastapi import Header, HTTPException, Request, status
from jose import JWTError, jwt
from passlib.context import CryptContext

from src.core import get_settings
from src.crud.base import CRUDBase
from src.schema import CreateAdmin, UpdateAdmin


class CRUDAdmin(CRUDBase[CreateAdmin, UpdateAdmin]):
    def __init__(self, collection: str) -> None:
        super().__init__(collection)
        self.password_context = CryptContext(
            schemes=["bcrypt"], deprecated="auto"
        )

    async def auth_user(
        self,
        request: Request,
        Authorization=Header(..., description="관리자 계정의 액세스 토큰 값"),
    ) -> bool:
        """
        관리자 계정 액세스 토큰 확인 메서드
        """
        try:
            payload = jwt.decode(
                token=Authorization,
                key=get_settings().SECRET_KEY,
                algorithms=[get_settings().ALGORITHM],
            )
            admin_id = payload.get("sub")
            if not admin_id:
                raise HTTPException(
                    detail="Access Token Not Found",
                    status_code=status.HTTP_403_FORBIDDEN,
                )

            elif not request.app.db[self.collection].find_one(
                {"admin_id": admin_id}
            ):
                raise HTTPException(
                    detail="Admin User Not Found",
                    status_code=status.HTTP_403_FORBIDDEN,
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
        """
        관리자 계정 조회 메서드
        """
        user = await request.app.db[self.collection].find_one(
            {"admin_id": user_data.admin_id}
        )

        if not user:
            return None

        elif not self.password_context.verify(
            secret=user_data.admin_password, hash=user["admin_password"]
        ):
            raise HTTPException(
                detail="Unauthorized", status_code=status.HTTP_401_UNAUTHORIZED
            )

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
        """
        관리자 계정 생성 메서드
        """
        insert_data.admin_password = self.password_context.hash(
            secret=insert_data.admin_password
        )
        result = await super().create(request=request, insert_data=insert_data)

        return result


admin_crud = CRUDAdmin(collection="admin")
