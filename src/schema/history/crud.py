from src.schema.crud import CreateSchemaBase, CRUDSchemaBase, UpdateSchemaBase


class HistoryBase(CRUDSchemaBase):
    history_year: int | None
    history_month: int | None
    history_content: str | None


class CreateHistory(HistoryBase, CreateSchemaBase):
    history_year: int
    history_month: int
    history_content: str

    class Config:
        schema_extra: dict[str, dict] = {"example": {}}


class UpdateHistory(HistoryBase, UpdateSchemaBase):
    history_id: str

    class Config:
        schema_extra: dict[str, dict] = {"example": {}}
