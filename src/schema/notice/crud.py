from enum import Enum

from src.schema.crud_base import BaseSchema


class NoticeType(str, Enum):
    """
    공지사항 및 자료실 종류 이넘(Enum) 클래스
    """

    ARCHIVE = "archive"
    NOTIFICATION = "notification"


class NoticeBase(BaseSchema):
    """
    공지사항 및 자료실 기본 스키마
    """

    notice_type: NoticeType | None
    notice_title: str | None
    notice_content: str | None
    notice_files: list[dict[str, str]] | None
    notice_images: list[dict[str, str]] | None


class CreateNotice(NoticeBase):
    """
    공지사항 및 자료실 생성 스키마
    """

    notice_type: NoticeType
    notice_title: str
    notice_content: str

    class Config:
        schema_extra: dict[str, dict] = {"example": {}}


class UpdateNotice(NoticeBase):
    """
    공지사항 및 자료실 수정 스키마
    """

    class Config:
        schema_extra: dict[str, dict] = {"example": {}}
