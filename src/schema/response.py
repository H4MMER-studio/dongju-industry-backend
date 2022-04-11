from pydantic import BaseModel


class GetResponseModel(BaseModel):
    data: list[dict] | dict[str, str | int] | None


class AlterResponseModel(BaseModel):
    detail: str


class ErrorResponseModel(BaseModel):
    detail: str | list[dict[str, str]]
