from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse

SINGLE_PREFIX = "/admin"

router = APIRouter(prefix=SINGLE_PREFIX)


@router.post("/sign-up")
async def sign_up(request: Request):
    try:

        return JSONResponse()

    except Exception as error:
        return JSONResponse(
            content={"detail": str(error)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.post("/sign-in")
async def sing_in(request: Request):
    try:
        return JSONResponse()

    except Exception as error:
        return JSONResponse(
            content={"detail": str(error)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
