from enum import Enum

from src.schema.crud import CreateSchemaBase, CRUDSchemaBase, UpdateSchemaBase


class CertificationType(str, Enum):
    LICENSE = "등록증"
    CERTIFICATION = "주요 인증"
    PATENT = "특허증"
    TEST_RESULT = "시험성적서"


class CertificationBase(CRUDSchemaBase):
    certification_type: CertificationType | None
    certification_title: str | None
    certification_content: str | None
    certification_date: str | None
    certification_organization: str | None
    certification_images: list[dict[str, str]] | None


class CreateCertification(CertificationBase, CreateSchemaBase):
    certification_type: CertificationType
    certification_title: str
    certification_images: list[dict[str, str]]

    class Config:
        schema_extra: dict[str, dict] = {"example": {}}


class UpdateCertification(CertificationBase, UpdateSchemaBase):
    class Config:
        schema_extra: dict[str, dict] = {"example": {}}
