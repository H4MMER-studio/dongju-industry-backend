from bson.objectid import InvalidId
from fastapi import APIRouter, Query, Request, status
from fastapi.responses import JSONResponse

from src.crud import history_crud
from src.schema import CreateHistory, UpdateHistory

SINGLE_PREFIX = "/history"
PLURAL_PREFIX = "/histories"

router = APIRouter()


@router.get(PLURAL_PREFIX)
async def get_histories(
    request: Request,
    skip: int = Query(default=0),
    limit: int = Query(default=0),
    sort: list[str] = Query(
        default=["history-year desc", "history-month desc"]
    ),
) -> JSONResponse:
    try:

        if result := await history_crud.get_multi(
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


@router.post(SINGLE_PREFIX)
async def create_history(
    request: Request, insert_data: CreateHistory
) -> JSONResponse:
    try:
        await history_crud.create(request=request, insert_data=insert_data)

        return JSONResponse(
            content={"detail": "Success"}, status_code=status.HTTP_200_OK
        )

    except Exception as error:
        return JSONResponse(
            content={"detail": error},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.patch(PLURAL_PREFIX)
async def update_history(
    request: Request, update_data: list[UpdateHistory]
) -> JSONResponse:
    try:

        if await history_crud.bulk_update(
            request=request, update_data=update_data, model="history"
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


@router.delete(PLURAL_PREFIX)
async def delete_history(
    request: Request, history_ids: list[str]
) -> JSONResponse:
    try:
        if await history_crud.bulK_delete(request=request, ids=history_ids):
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
