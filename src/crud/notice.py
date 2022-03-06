from src.crud.base import CRUDBase
from src.schema import CreateNotice, UpdateNotice


class CRUDNotice(CRUDBase[CreateNotice, UpdateNotice]):
    pass


notice_crud = CRUDNotice(collection="notices")
