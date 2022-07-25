from pydantic import BaseModel


class AdminBase(BaseModel):
    admin_id: str | None
    admin_password: str | None


class CreateAdmin(AdminBase):
    admin_id: str
    admin_password: str

    class Config:
        schema_extra: dict[str, dict] = {
            "example": {
                "admin_id": "testId",
                "admin_password": "testPassword",
            }
        }


class UpdateAdmin(AdminBase):
    class Config:
        schema_extra: dict[str, dict] = {"example": {}}
