from datetime import date
from enum import Enum

from src.schema.crud import CreateSchemaBase, CRUDSchemaBase, UpdateSchemaBase


class CertificationType(str, Enum):
    LICENSE = "license"
    CERTIFICATION = "core-certification"
    PATENT = "patent"
    TEST_RESULT = "test-result"


class CertificationBase(CRUDSchemaBase):
    certification_type: CertificationType | None
    certification_title: str | None
    certification_content: str | None
    certification_start_date: date | None
    certification_end_date: date | None
    certification_organization: str | None
    certification_images: list[dict[str, str]] | None


class CreateCertification(CreateSchemaBase, CertificationBase):
    certification_type: CertificationType
    certification_title: str
    certification_images: list[dict[str, str]]


class UpdateCertification(UpdateSchemaBase, CertificationBase):
    class Config:
        schema_extra: dict[str, dict] = {"example": {}}
