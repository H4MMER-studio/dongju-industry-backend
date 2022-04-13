from bson.objectid import InvalidId
from fastapi import APIRouter, Query, Request, status
from fastapi.responses import JSONResponse

from src.crud import delivery_crud
from src.schema import (
    CreateDelivery,
    UpdateDelivery,
    create_delivery_response,
    delete_response,
    get_deliveries_response,
    update_response,
)

SINGLE_PREFIX = "/delivery"
PLURAL_PREFIX = "/deliveries"

router = APIRouter()


@router.get(PLURAL_PREFIX, responses=get_deliveries_response)
async def get_deliveries(
    request: Request,
    skip: int = Query(default=0),
    limit: int = Query(default=0),
    sort: list[str] = Query(
        default=[
            "delivery-year asc",
            "delivery-month asc",
            "delivery-supplier asc",
            "delivery-amount asc",
        ]
    ),
) -> JSONResponse:
    """
    납품실적 다량 조회(GET) 엔드포인트

    아래 세 개의 매개변수는 선택적으로 전달할 수 있는 쿼리 파라미터(Query Parameter)
    1. sort
    2. skip
    3. limit

    이때 기본적으로 납품연도, 납품월, 납품처, 납품량 순서로 오름차순 정렬하여 결과를 반환한다.
    """
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


@router.post(SINGLE_PREFIX, responses=create_delivery_response)
async def create_delivery(
    request: Request, insert_data: CreateDelivery
) -> JSONResponse:
    """
    납품실적 생성(CREATE) 엔드포인트

    아래 네 개는 필수적으로 전달해야 하는 바디 파라미터(Body Parameter)

    1. delivery_supplier
    2. delivery_product
    3. delivery_amount
    4. delivery_year

    아래 두 개는 선택적으로 전달할 수 있는 바디 파라미터(Body Parameter)
    1. delivery_month
    2. delivery_reference
    """
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


@router.patch(SINGLE_PREFIX + "/{delivery_id}", responses=update_response)
async def update_delivery_partialy(
    request: Request, delivery_id: str, update_data: UpdateDelivery
) -> JSONResponse:
    """
    납품실적 수정(PATCH) 엔드포인트

    아래 한 개는 필수적으로 전달해야하는 패스 파라미터(Path Parameter)
    1. _id

    아래 여섯 개는 선택적으로 전달할 수 있는 바디 마라미터(Body Parameter)
    1. delivery_supplier
    2. delivery_product
    3. delivery_amount
    4. delivery_year
    5. delivery_month
    6. delivery_reference
    """
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


@router.delete(SINGLE_PREFIX + "/{delivery_id}", responses=delete_response)
async def delete_delivery(request: Request, delivery_id: str) -> JSONResponse:
    """
    납품실적 삭제(DELETE) 엔드포인트

    아래 한 개는 필수적으로 전달해야하는 패스 파라미터(Path Parameter)
    1. _id
    """
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
