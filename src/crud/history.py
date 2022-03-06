from src.crud.base import CRUDBase
from src.schema import CreateHistory, UpdateHistory


class CRUDHistory(CRUDBase[CreateHistory, UpdateHistory]):
    pass


history_crud = CRUDHistory(collection="histories")
