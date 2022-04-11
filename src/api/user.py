from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

SINGLE_PREFIX = "/user"

router = APIRouter(prefix=SINGLE_PREFIX)


@router.post("")
async def create_user(request: Request):
    return JSONResponse()
