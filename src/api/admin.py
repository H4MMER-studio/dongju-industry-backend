from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse

from src.crud import admin_crud
from src.schema import CreateAdmin

SINGLE_PREFIX = "/admin"

router = APIRouter(prefix=SINGLE_PREFIX)


@router.post(path="/sign-up")
async def sign_up(request: Request, insert_data: CreateAdmin) -> JSONResponse:
    try:
        if await admin_crud.create(request=request, insert_data=insert_data):
            return JSONResponse(
                content={"detail": "success"}, status_code=status.HTTP_200_OK
            )

        else:
            return JSONResponse(
                content={"detail": "Database Error"},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    except Exception as error:
        return JSONResponse(
            content={"detail": str(error)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.post(path="/sign-in")
async def sing_in(request: Request, user_data: CreateAdmin) -> JSONResponse:
    """
    사용자 로그인

    """
    try:
        if result := await admin_crud.get_one(
            request=request, user_data=user_data
        ):
            return JSONResponse(
                content={"data": result}, status_code=status.HTTP_200_OK
            )

        else:
            return JSONResponse(
                content={"data": []}, status_code=status.HTTP_200_OK
            )

    except Exception as error:
        return JSONResponse(
            content={"detail": str(error)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
