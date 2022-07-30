from bson.objectid import InvalidId
from fastapi import APIRouter, Body, Depends, Query, Request, status
from fastapi.responses import JSONResponse

from src.crud import admin_crud, delivery_crud
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
    skip: int = Query(default=0, description="페이지네이션 시작 값", example=1),
    limit: int = Query(default=0, description="페이지네이션 종료 값", example=30),
    sort: list[str] = Query(
        default=[
            "delivery-year asc",
            "delivery-month asc",
            "delivery-supplier asc",
            "delivery-amount asc",
        ],
        description="정렬 기준",
        example=["delivery-year desc", "delivery-month desc"],
    ),
    type: str = Query(default=None, description="조회 방법", example="search"),
    field: str = Query(
        default=None, description="검색 대상이 되는 필드", example="delivery-supplier"
    ),
    value: str = Query(default=None, description="검색어", example="ㄷㅓㄱㅅㅏㄴ"),
) -> JSONResponse:
    """
    납품실적 다량 조회(GET) 엔드포인트

    아래 여섯 개는 선택적으로 전달할 수 있는 쿼리 파라미터(Query Parameter)
    1. sort
    2. skip
    3. limit
    4. type
    5. field
    6. value

    이때 type 쿼리 파라미터의 경우 아래와 같이 두 가지 값을 가질 수 있습니다.
    1. null : 기본적인 다량 조회
    2. search : 키워드 검색

    field 쿼리 파라미터의 경우 아래와 같이 두 가지 값을 가질 수 있다.
    1. 납품처(delivery_supplier)
    2. 품명(delivery_product)

    이때 기본적으로 아래 순서를 기준으로 오름차순 정렬하여 결과를 반환한다.
    1. 납품연도(delivery_year)
    2. 납품월(delivery_month)
    3. 납품처(delivery_supplier)
    4. 납품량(delivery_amount)
    """
    try:
        result = await delivery_crud.get_multi(
            request=request,
            skip=skip,
            limit=limit,
            sort=sort,
            type=type,
            field=field,
            value=value,
        )
        if result["size"]:
            return JSONResponse(
                content=result,
                status_code=status.HTTP_200_OK,
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


@router.post(
    path=SINGLE_PREFIX,
    responses=create_delivery_response,
    dependencies=[Depends(admin_crud.auth_user)],
)
async def create_delivery(
    request: Request,
    type: str = Query(default=None),
    insert_data: CreateDelivery | bytes = Body(default=None),
) -> JSONResponse:
    """
    납품실적 생성(POST) 엔드포인트

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
        if type == "file":
            if await delivery_crud.bulk_create(
                request=request, insert_data=insert_data
            ):
                return JSONResponse(
                    content={"detail": "Success"},
                    status_code=status.HTTP_200_OK,
                )

            else:
                return JSONResponse(
                    content={"detail": "Database Error"},
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        else:
            if await delivery_crud.create(
                request=request, insert_data=insert_data
            ):
                return JSONResponse(
                    content={"detail": "Success"},
                    status_code=status.HTTP_200_OK,
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


@router.patch(
    path=SINGLE_PREFIX + "/{delivery_id}",
    responses=update_response,
    dependencies=[Depends(admin_crud.auth_user)],
)
async def update_delivery_partialy(
    request: Request, delivery_id: str, update_data: UpdateDelivery
) -> JSONResponse:
    """
    납품실적 수정(PATCH) 엔드포인트

    아래 한 개는 필수적으로 전달해야 하는 패스 파라미터(Path Parameter)
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
                content={"data": []}, status_code=status.HTTP_200_OK
            )

    except InvalidId as invalid_id_error:
        return JSONResponse(
            content={"detail": str(invalid_id_error)},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    except Exception as error:
        return JSONResponse(
            content={"detail": str(error)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.delete(
    path=SINGLE_PREFIX + "/{delivery_id}",
    responses=delete_response,
    dependencies=[Depends(admin_crud.auth_user)],
)
async def delete_delivery(request: Request, delivery_id: str) -> JSONResponse:
    """
    납품실적 삭제(DELETE) 엔드포인트

    아래 한 개는 필수적으로 전달해야 하는 패스 파라미터(Path Parameter)
    1. _id
    """
    try:
        if await delivery_crud.delete(request=request, id=delivery_id):
            return JSONResponse(
                content={"detail": "Success"}, status_code=status.HTTP_200_OK
            )
        else:
            return JSONResponse(
                content={"data": []}, status_code=status.HTTP_200_OK
            )

    except InvalidId as invalid_id_error:
        return JSONResponse(
            content={"detail": str(invalid_id_error)},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    except Exception as error:
        return JSONResponse(
            content={"detail": str(error)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
