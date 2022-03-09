from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse

from src.crud import certification_crud  # noqa
from src.schema import CreateCertification, UpdateCertification  # noqa

router = APIRouter()


@router.get("")
async def get_certification(certification_id: str, request: Request):
    try:
        certification_crud.get_one(id=certification_id, request=request)

    except TypeError:
        return JSONResponse(
            content={"detail": "{certification_id} Invalid"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    except Exception as error:
        return JSONResponse(
            content={"detail": error},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.get("s")
async def get_certifications(request: Request):
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
