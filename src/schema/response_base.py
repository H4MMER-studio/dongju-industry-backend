from pydantic import BaseModel


class GetResponseModel(BaseModel):
    """
    조회 응답 관련 스키마
    """

    data: list[dict] | dict[str, str | int] | None


class AlterResponseModel(BaseModel):
    """
    수정 및 생성 응답 관련 스키마
    """

    detail: str


class ErrorResponseModel(BaseModel):
    """
    오류 응답 관련 스키마
    """

    detail: str | list[dict[str, str]]
