from pydantic import BaseModel


class HistoryBase(BaseModel):
    history_year: int | None
    history_month: int | None
    history_content: str | None


class CreateHistory(HistoryBase):
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
    history_id: str
