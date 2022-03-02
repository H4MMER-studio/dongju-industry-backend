from datetime import date
from typing import Optional

from pydantic import BaseModel


class CertificationBase(BaseModel):
    """
    To Do
    - 일자의 경우 문자열형으로 저장할 것인지 아니면 날짜 데이터로 저장할 것인지 고민
    """

    title: str
    content: Optional[str]
    date: Optional[date]
    organization: Optional[str]
    image: str


class CreateCertification(CertificationBase):
    class Config:
        schema_extra = {"example": {}}


class UpdateCertification(CertificationBase):
    title: Optional[str]
    image: Optional[str]

    class Config:
        schema_extra = {"example": {}}
