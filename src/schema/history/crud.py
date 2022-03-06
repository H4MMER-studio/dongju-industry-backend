from src.schema.crud import CRUDSchemaBase


class HistoryBase(CRUDSchemaBase):
    history_yaer: str | None
    history_month: str | None
    history_content: str | None


class CreateHistory(HistoryBase):
    history_year: str
    history_month: str
    history_content: str

    class Config:
        schema_extra: dict[str, dict] = {"example": {}}


class UpdateHistory(HistoryBase):
    class Config:
        schema_extra: dict[str, dict] = {"example": {}}
