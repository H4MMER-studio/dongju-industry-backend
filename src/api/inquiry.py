from bson.objectid import InvalidId
from fastapi import APIRouter, Query, Request, status
from fastapi.responses import JSONResponse

from src.crud import inquiry_crud
from src.schema import CreateInquiry

router = APIRouter()


@router.get("/inquiry/{inquiry_id}")
async def get_inquiry(request: Request, inquiry_id: str):
    try:
        if result := await inquiry_crud.get_one(
            request=request, id=inquiry_id
        ):
            return JSONResponse(
                content={"data": result}, status_code=status.HTTP_200_OK
            )

        else:
            return JSONResponse(
                content={"data": []}, status_code=status.HTTP_404_NOT_FOUND
            )

    except InvalidId as invalid_id_error:
        return JSONResponse(
            content={"detail": str(invalid_id_error)},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    except Exception as error:
        return JSONResponse(
            content={"detail": error},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.get("/inquiries")
async def get_inquries(
    request: Request,
    skip: int | None = Query(default=0),
    limit: int | None = Query(default=0),
    sort: list[str] = Query(default=["created-at asc"]),
) -> JSONResponse:
    try:
        if result := await inquiry_crud.get_multi(
            request=request, skip=skip, limit=limit, sort=sort
        ):
            return JSONResponse(
                content={"data": result}, status_code=status.HTTP_200_OK
            )

        else:
            return JSONResponse(
                content={"data": []}, status_code=status.HTTP_404_NOT_FOUND
            )

    except Exception as error:
        return JSONResponse(
            content={"detail": error},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.post("/inquiry")
async def create_inquiry(
    request: Request, insert_data: CreateInquiry
) -> JSONResponse:
    try:
        await inquiry_crud.create(request=request, insert_data=insert_data)

        return JSONResponse(
            content={"detail": "Success"}, status_code=status.HTTP_200_OK
        )

    except Exception as error:
        return JSONResponse(
            content={"detail": error},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
