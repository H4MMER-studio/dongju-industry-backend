from datetime import date
from enum import Enum

from src.schema.crud_base import BaseSchema


class CertificationType(str, Enum):
    """
    인증서 종류 이넘(Enum) 클래스
    """

    LICENSE = "license"
    CERTIFICATION = "core-certification"
    PATENT = "patent"
    TEST_RESULT = "test-result"


class CertificationBase(BaseSchema):
    """
    인증서 기본 스키마
    """

    certification_type: CertificationType | None
    certification_title: str | None
    certification_content: str | None
    certification_start_date: date | None
    certification_end_date: date | None
    certification_organization: str | None
    certification_images: list[dict[str, str]] | None


class CreateCertification(CertificationBase):
    """
    인증서 생성 스키마
    """

    certification_type: CertificationType
    certification_title: str
    certification_images: list[dict[str, str]]

    class Config:
        schema_extra: dict[str, dict] = {
            "example": {
                "ceritification_type": "",
                "certification_title": "",
                "certification_images": [],
            }
        }


class UpdateCertification(CertificationBase):
    """
    인증서 수정 스키마
    """

    class Config:
        schema_extra: dict[str, dict] = {
            "example": {"certification_title": "수정하려는 인증서 제목"}
        }
