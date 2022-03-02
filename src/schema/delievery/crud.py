from datetime import date
from typing import Optional

from pydantic import BaseModel


class DelieveryBase(BaseModel):
    """
    To Do
    - 납품일자의 경우 문자열형으로 저장할 것인지 아니면 날짜 데이터로 저장할 것인지 고민
    """

    supplier: str
    product: str
    amount: int
    date: date
    reference: Optional[str]


class CreateDelievery(DelieveryBase):
    class Config:
        schema_extra = {"example": {}}


class UpdateDelievery(DelieveryBase):
    supplier: Optional[str]
    product: Optional[str]
    amount: Optional[int]
    date: Optional[date]

    class Config:
        schema_extra = {"example": {}}
