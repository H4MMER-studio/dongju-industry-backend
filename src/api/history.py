from bson.objectid import InvalidId
from fastapi import APIRouter, Body, Depends, Query, Request, status
from fastapi.responses import JSONResponse

from src.crud import admin_crud, history_crud
from src.schema import (
    CreateHistory,
    UpdateHistory,
    create_history_response,
    delete_response,
    get_histories_response,
    update_response,
)

SINGLE_PREFIX = "/history"
PLURAL_PREFIX = "/histories"

router = APIRouter()


@router.get(path=PLURAL_PREFIX, responses=get_histories_response)
async def get_histories(
    request: Request,
    skip: int = Query(default=0, description="페이지네이션 시작 값", example=1),
    limit: int = Query(default=0, desciption="페이지네이션 종료 값", example=30),
    sort: list[str] = Query(
        default=["history-year desc", "history-month desc", "created_at desc"],
        description="정렬 기준",
        example=["history-year desc", "history-month desc"],
    ),
) -> JSONResponse:
    """
    연혁 종류별 다량 조회(GET) 엔드포인트

    아래 한 개는 선택적으로 전달할 수 있는 쿼리 파라미터(Query Parameter)
    1. sort

    이때 기본적으로 아래 기준으로 내림차순 정렬하여 결과를 반환한다.
    1. 연혁연도(history_year)
    2. 연혁월(history_month)
    3. 엔티티 생성일(created_at)
    """
    try:
        result = await history_crud.get_multi(
            request=request,
            skip=skip,
            limit=limit,
            sort=sort,
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
    responses=create_history_response,
    dependencies=[Depends(admin_crud.auth_user)],
)
async def create_history(
    request: Request, insert_data: CreateHistory
) -> JSONResponse:
    """
    연혁 생성(POST) 엔드포인트

    아래 세 개는 필수적으로 전달해야 하는 바디 파라미터(Body Parameter)
    1. history_year
    2. history_month
    3. history_content
    """
    try:
        if await history_crud.create(request=request, insert_data=insert_data):
            return JSONResponse(
                content={"detail": "Success"}, status_code=status.HTTP_200_OK
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
    path=PLURAL_PREFIX,
    responses=update_response,
    dependencies=[Depends(admin_crud.auth_user)],
)
async def update_history(
    request: Request,
    update_data: list[UpdateHistory] = Body(
        ...,
        desciprtion="수정하고자 하는 연력 아이디 및 데이터를 담은 배열",
        example=[
            {"history_id": "624db4d66a6b5d4406086415", "history_year": 2018},
            {
                "history_id": "624db4df6a6b5d4406086416",
                "history_content": "주식회사 동주산업 법인 설립",
            },
        ],
    ),
) -> JSONResponse:
    """
    연혁 다량 수정(PATCH) 엔드포인트

    배열에 객체 형태로 수정하고자 하는 연혁의 _id 값 및 데이터를 담아 전달한다.

    아래 한 개는 객체에 필수적으로 존재해야 하는 키
    1. history_id

    아래 세 개는 객체에 선택적으로 존재할 수 있는 키
    1. history_year
    2. history_month
    3. history_content
    """
    try:

        if await history_crud.bulk_update(
            request=request, update_data=update_data
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
    path=PLURAL_PREFIX,
    responses=delete_response,
    dependencies=[Depends(admin_crud.auth_user)],
)
async def delete_history(
    request: Request,
    history_ids: list[str] = Body(
        ...,
        description="삭제하고자 하는 연혁 아이디를 담은 배열",
        example=["624db4e86a6b5d4406086417", "624db4d66a6b5d4406086415"],
    ),
) -> JSONResponse:
    """
    연혁 다량 삭제(DELETE) 엔드포인트

    배열에 삭제하고자 하는 연혁의 _id 값을 담아 전달한다.
    """
    try:
        if await history_crud.bulk_delete(request=request, ids=history_ids):
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
