from bson.objectid import InvalidId
from fastapi import APIRouter, Query, Request, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from src.crud import notice_crud
from src.schema import CreateNotice, UpdateNotice
from src.util import parse_formdata

router = APIRouter()


@router.get("/{notice_id}")
async def get_notice(request: Request, notice_id: str) -> JSONResponse:
    try:
        if result := await notice_crud.get_one(request=request, id=notice_id):
            return JSONResponse(
                content={"data": result}, status_code=status.HTTP_200_OK
            )

        else:
            return JSONResponse(
                content={"detail", "Not Found"},
                status_code=status.HTTP_404_NOT_FOUND,
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


@router.get("s")
async def get_notices(
    request: Request,
    skip: int = Query(default=0),
    limit: int = Query(default=0),
    sort: list[str] = Query(default=["created-at asc"]),
) -> JSONResponse:
    try:
        if result := await notice_crud.get_multi(
            request=request, skip=skip, limit=limit, sort=sort
        ):
            return JSONResponse(
                content={"data": result}, status_code=status.HTTP_200_OK
            )

        else:
            return JSONResponse(
                content={"detail": "Not Found"},
                status_code=status.HTTP_404_NOT_FOUND,
            )

    except Exception as error:
        return JSONResponse(
            content={"detail": error},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.post("")
async def create_notice(request: Request) -> JSONResponse:
    try:
        form_data = await request.form()
        insert_data = await parse_formdata(
            form_data=form_data,
            create_schema=CreateNotice,
            collection_name="notice",
        )

        await notice_crud.create(insert_data=insert_data, request=request)

        return JSONResponse(
            content={"detail": "Success"}, status_code=status.HTTP_200_OK
        )

    except ValidationError as validation_error:
        return JSONResponse(
            content={"detail": validation_error.errors()},
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    except Exception as error:
        return JSONResponse(
            content={"detail": error},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.patch("/{notice_id}")
async def update_notice_partialy(
    request: Request, notice_id: str, update_data: UpdateNotice
) -> JSONResponse:
    try:
        if await notice_crud.update(
            request=request, id=notice_id, update_data=update_data
        ):
            return JSONResponse(
                content={"detail": "Success"}, status_code=status.HTTP_200_OK
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


@router.delete("/{notice_id}")
async def delete_notice(request: Request, notice_id: str) -> JSONResponse:
    try:
        if await notice_crud.delete(request=request, id=notice_id):
            return JSONResponse(
                content={"detail": "Success"}, status_code=status.HTTP_200_OK
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
