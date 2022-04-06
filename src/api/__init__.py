from fastapi import APIRouter

from src.api import (
    certification,
    delivery,
    file,
    history,
    inquiry,
    notice,
    search,
)

router = APIRouter(prefix="/v1")

router.include_router(router=file.router, prefix="/file", tags=["File"])
router.include_router(router=search.router, prefix="/search", tags=["Search"])
router.include_router(
    router=inquiry.router, prefix="/inquiry", tags=["Inquiry"]
)
router.include_router(router=notice.router, prefix="/notice", tags=["Notice"])
router.include_router(
    router=history.router, prefix="/history", tags=["History"]
)
router.include_router(
    router=delivery.router, prefix="/delivery", tags=["Delivery"]
)
router.include_router(
    router=certification.router, prefix="/certification", tags=["Certification"]
)