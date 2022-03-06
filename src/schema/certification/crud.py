from enum import Enum

from src.schema.crud import CRUDSchemaBase


class CertificationType(Enum, str):
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
    certification_image: str | None


class CreateCertification(CertificationBase):
    certification_type: CertificationType
    certification_title: str
    certification_image: str

    class Config:
        schema_extra: dict[str, dict] = {"example": {}}


class UpdateCertification(CertificationBase):
    class Config:
        schema_extra: dict[str, dict] = {"example": {}}
