from datetime import datetime, timedelta, timezone
from typing import Optional

from pydantic import BaseModel


class CRUDSchemaBase(BaseModel):
    created_at: datetime = datetime.now(tz=timezone(offset=timedelta(hours=9)))
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
