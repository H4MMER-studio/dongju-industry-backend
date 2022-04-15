from pydantic import EmailStr

from src.schema.crud import CreateSchemaBase, CRUDSchemaBase, UpdateSchemaBase


class UserBase(CRUDSchemaBase):
    user_id: str | None
    user_email: EmailStr | None
    user_password: str | None


class CreateUser(UserBase, CreateSchemaBase):
    user_id: str
    user_email: EmailStr
    user_password: str

    class Config:
        schema_extra: dict[str, dict] = {
            "example": {
                "user_id": "dongju-id",
                "user_email": "dongju-test@dongju.com",
                "user_password": "dongju-password",
            }
        }


class UpdateUser(UserBase, UpdateSchemaBase):
    class Config:
        schema_extra: dict[str, dict] = {"example": {}}
