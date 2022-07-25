from datetime import date
from enum import Enum

from pydantic import BaseModel


class CertificationType(str, Enum):
    LICENSE = "license"
    CERTIFICATION = "core-certification"
    PATENT = "patent"
    TEST_RESULT = "test-result"


class CertificationBase(BaseModel):
    certification_type: CertificationType | None
    certification_title: str | None
    certification_content: str | None
    certification_start_date: date | None
    certification_end_date: date | None
    certification_organization: str | None
    certification_images: list[dict[str, str]] | None


class CreateCertification(CertificationBase):
    certification_type: CertificationType
    certification_title: str
    certification_images: list[dict[str, str]]


class UpdateCertification(CertificationBase):
    class Config:
        schema_extra: dict[str, dict] = {"example": {}}
