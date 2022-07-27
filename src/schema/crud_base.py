from datetime import datetime

from pydantic import BaseModel


class BaseSchema(BaseModel):
    """
    기본 스키마
    """

    created_at: datetime | None
    updated_at: datetime | None
    deleted_at: datetime | None
