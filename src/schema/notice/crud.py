from enum import Enum

from src.schema.crud import CreateSchemaBase, CRUDSchemaBase, UpdateSchemaBase


class NoticeType(str, Enum):
    ARCHIVE = "archive"
    NOTIFICATION = "notification"


class NoticeBase(CRUDSchemaBase):
    notice_type: NoticeType | None
    notice_title: str | None
    notice_content: str | None
    notice_files: list[dict[str, str]] | None
    notice_images: list[dict[str, str]] | None


class CreateNotice(CreateSchemaBase, NoticeBase):
    notice_type: NoticeType
    notice_title: str
    notice_content: str

    class Config:
        schema_extra: dict[str, dict] = {"example": {}}


class UpdateNotice(UpdateSchemaBase, NoticeBase):
    class Config:
        schema_extra: dict[str, dict] = {"example": {}}
