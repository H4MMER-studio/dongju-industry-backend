from src.schema.crud_base import BaseSchema


class HistoryBase(BaseSchema):
    """
    연혁 기본 스키마
    """

    history_year: int | None
    history_month: int | None
    history_content: str | None


class CreateHistory(HistoryBase):
    """
    연혁 생성 스키마
    """

    history_year: int
    history_month: int
    history_content: str

    class Config:
        schema_extra: dict[str, dict] = {
            "example": {
                "history_year": 1999,
                "history_month": 2,
                "history_content": "동주산업 제 2공장 설립 (인천 가좌동 소재)",
            }
        }


class UpdateHistory(HistoryBase):
    """
    연혁 수정 스키마
    """

    history_id: str

    class Config:
        schema_exatra: dict[str, dict] = {
            "example": {"history_content": "수정할 연혁 내용"}
        }
