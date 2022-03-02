from typing import Optional

from pydantic import BaseModel


class HistoryBase(BaseModel):
    yaer: str
    month: str
    content: str


class CreateHistory(HistoryBase):
    class Config:
        schema_extra = {"example": {}}


class UpdateHistory(HistoryBase):
    year: Optional[str]
    month: Optional[str]
    content: Optional[str]

    class Config:
        schema_extra = {"example": {}}
