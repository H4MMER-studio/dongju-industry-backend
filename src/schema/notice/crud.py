from enum import Enum

from src.schema.crud import CreateSchemaBase, CRUDSchemaBase, UpdateSchemaBase


class NoticeType(str, Enum):
    ARCHIVE = "자료실"
    NOTIFICATION = "공지사항"


class NoticeBase(CRUDSchemaBase):
    """
    To Do
    - 텍스트 에디터에 삽입하는 이미지를 어떻게 할 것인지 논의 필요
    - 데이터의 경우 자료실에서 사용되는 것
    """

    notice_type: NoticeType | None
    notice_title: str | None
    notice_content: str | None
    notice_files: list[dict[str, str]] | None


class CreateNotice(CreateSchemaBase, NoticeBase):
    notice_type: NoticeType
    notice_title: str
    notice_content: str

    class Config:
        schema_extra: dict[str, dict] = {"example": {}}


class UpdateNotice(UpdateSchemaBase, NoticeBase):
    class Config:
        schema_extra: dict[str, dict] = {"example": {}}
