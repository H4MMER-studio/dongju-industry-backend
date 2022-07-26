from src.crud.base import CRUDBase
from src.schema import CreateCertification, UpdateCertification


class CRUDCertification(CRUDBase[CreateCertification, UpdateCertification]):
    pass


certification_crud = CRUDCertification(collection="certifications")
