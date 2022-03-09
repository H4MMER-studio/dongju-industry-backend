from fastapi import APIRouter

from src.api import certification

router = APIRouter(prefix="/v1")


router.include_router(
    router=certification.router, prefix="/certification", tags=["Certication"]
)
