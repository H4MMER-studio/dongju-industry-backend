from enum import Enum

from pydantic import BaseModel


class NoticeType(str, Enum):
    ARCHIVE = "archive"
    NOTIFICATION = "notification"


class NoticeBase(BaseModel):
    notice_type: NoticeType | None
    notice_title: str | None
    notice_content: str | None
    notice_files: list[dict[str, str]] | None
    notice_images: list[dict[str, str]] | None


class CreateNotice(NoticeBase):
    notice_type: NoticeType
    notice_title: str
    notice_content: str

    class Config:
        schema_extra: dict[str, dict] = {"example": {}}


class UpdateNotice(NoticeBase):
    class Config:
        schema_extra: dict[str, dict] = {"example": {}}
