from src.crud.base import CRUDBase
from src.schema import CreateInquiry, UpdateInquiry


class CRUDIquiry(CRUDBase[CreateInquiry, UpdateInquiry]):
    pass


inquiry_crud = CRUDIquiry(collection="inquiries")
