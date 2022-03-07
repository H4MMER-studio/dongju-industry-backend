from fastapi import APIRouter

from src.crud import certification_crud  # noqa
from src.schema import CreateCertification, UpdateCertification  # noqa

router = APIRouter()


@router.get("")
async def get_certification():
    pass


@router.get("s")
async def get_certifications():
    pass


@router.post("")
async def create_certification():
    pass


@router.patch("")
async def update_certification_partialy():
    pass


@router.delete("")
async def delete_certification():
    pass
