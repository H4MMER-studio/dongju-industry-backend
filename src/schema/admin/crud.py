from src.schema.crud_base import BaseSchema


class AdminBase(BaseSchema):
    """
    관리자 계정 기본 스키마
    """

    admin_id: str | None
    admin_password: str | None


class CreateAdmin(AdminBase):
    """
    관리자 계정 회원가입 및 로그인 스키마
    """

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
    """
    관리자 계정 수정 스키마
    """

    class Config:
        schema_extra: dict[str, dict] = {
            "example": {"admin_id": "수정하려는 관리자 계정 아이디"}
        }
