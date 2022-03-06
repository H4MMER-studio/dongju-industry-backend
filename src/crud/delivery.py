from src.crud.base import CRUDBase
from src.schema import CreateDelivery, UpdateDelivery


class CRUDDelivery(CRUDBase[CreateDelivery, UpdateDelivery]):
    pass


delivery_crud = CRUDDelivery(collection="deliveries")
