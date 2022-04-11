from bson.objectid import InvalidId
from fastapi import APIRouter, Query, Request, status
from fastapi.responses import JSONResponse

from src.crud import delivery_crud
from src.schema import CreateDelivery, UpdateDelivery

SINGLE_PREFIX = "/delivery"
PLURAL_PREFIX = "/deliveries"

router = APIRouter()


@router.get(PLURAL_PREFIX)
async def get_deliveries(
    request: Request,
    skip: int = Query(default=0),
    limit: int = Query(default=0),
    sort: list[str] = Query(
        default=[
            "delivery-year asc",
            "delivery-month asc",
            "delivery-reference asc",
            "delivery-amount asc",
        ]
    ),
) -> JSONResponse:
    try:
        if result := await delivery_crud.get_multi(
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
async def create_delivery(
    request: Request, insert_data: CreateDelivery
) -> JSONResponse:
    try:
        await delivery_crud.create(request=request, insert_data=insert_data)

        return JSONResponse(
            content={"detail": "Success"}, status_code=status.HTTP_200_OK
        )

    except Exception as error:
        return JSONResponse(
            content={"detail": error},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.patch(SINGLE_PREFIX + "/{delivery_id}")
async def update_delivery_partialy(
    request: Request, delivery_id: str, update_data: UpdateDelivery
) -> JSONResponse:
    try:
        if await delivery_crud.update(
            request=request, id=delivery_id, update_data=update_data
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


@router.delete(SINGLE_PREFIX + "/{delivery_id}")
async def delete_delivery(request: Request, delivery_id: str) -> JSONResponse:
    try:
        if await delivery_crud.delete(request=request, id=delivery_id):
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
