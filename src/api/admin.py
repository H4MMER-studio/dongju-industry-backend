from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse

from src.crud import admin_crud
from src.schema import CreateAdmin

SINGLE_PREFIX = "/admin"

router = APIRouter(prefix=SINGLE_PREFIX)


@router.post("/sign-up")
async def sign_up(request: Request, insert_data: CreateAdmin) -> JSONResponse:
    try:
        await admin_crud.create(request=request, insert_data=insert_data)

        return JSONResponse(
            content={"detail": "Success"}, status_code=status.HTTP_200_OK
        )

    except Exception as error:
        return JSONResponse(
            content={"detail": str(error)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.post("/sign-in")
async def sing_in(request: Request) -> JSONResponse:
    try:
        return JSONResponse()

    except Exception as error:
        return JSONResponse(
            content={"detail": str(error)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
