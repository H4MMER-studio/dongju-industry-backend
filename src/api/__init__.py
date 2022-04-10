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

router.include_router(router=file.router, prefix="/file", tags=["파일"])
router.include_router(router=search.router, prefix="/search", tags=["검색"])
router.include_router(router=inquiry.router, tags=["고객문의"])
router.include_router(router=notice.router, tags=["공지사항 및 자료실"])
router.include_router(router=history.router, tags=["연혁"])
router.include_router(router=delivery.router, tags=["납품실적"])
router.include_router(
    router=certification.router, prefix="certification", tags=["인증"]
)
