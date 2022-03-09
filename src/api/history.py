from fastapi import APIRouter
from fastapi.responses import JSONResponse  # noqa

from src.crud import history_crud  # noqa
from src.schema import CreateHistory, UpdateHistory  # noqa

router = APIRouter()


"""
To Do
- 일괄 수정
- 일괄 삭제
"""


@router.get("")
async def get_history():
    pass


@router.get("s")
async def get_histories():
    pass


@router.post("")
async def create_history():
    pass


@router.put("")
async def update_history():
    pass


@router.delete("")
async def delete_history():
    pass
