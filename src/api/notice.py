from bson.objectid import InvalidId
from fastapi import APIRouter, Depends, Query, Request, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from src.crud import admin_crud, notice_crud
from src.schema import (
    CreateNotice,
    NoticeType,
    UpdateNotice,
    create_response,
    delete_response,
    get_notice_response,
    get_notices_response,
    update_response,
)
from src.util import parse_formdata

SINGLE_PREFIX = "/notice"

router = APIRouter(prefix=SINGLE_PREFIX)


@router.get(path="/{notice_id}", responses=get_notice_response)
async def get_notice(request: Request, notice_id: str) -> JSONResponse:
    """
    공지 조회(GET) 엔드포인트

    아래 한 개는 필수적으로 전달해야 하는 패스 파라미터(Path Parameter)
    1. _id
    """
    try:
        result = await notice_crud.get_one(request=request, id=notice_id)
        if result["size"]:
            return JSONResponse(
                content=result,
                status_code=status.HTTP_200_OK,
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


@router.get(path="s", responses=get_notices_response)
async def get_notices(
    request: Request,
    value: NoticeType = Query(
        default=..., description="공지 종류", example="archive"
    ),
    skip: int = Query(default=0, description="페이지네이션 시작 값", example=1),
    limit: int = Query(default=0, description="페이지네이션 종료 값", example=30),
    sort: list[str] = Query(
        default=None,
        description="정렬 기준",
        example=["created-at desc"],
    ),
) -> JSONResponse:
    """
    공지 종류별 다량 조회(GET) 엔드포인트

    아래 한 개는 필수적으로 전달해야 하는 쿼리 파라미터(Query Parameter)
    1. value

    이때 그 값으로 공지종류(notice_type)를 전달한다.
    전달할 수 있는 공지종류는 아래와 같다.
    1. archive : 자료실
    2. notification : 공지사항

    아래 세 개는 선택적으로 전달할 수 있는 쿼리 파라미터(Query Parameter)
    1. sort
    2. skip
    3. limit

    이때 기본적으로 아래 기준으로 내림차순 정렬하여 결과를 반환한다.
    1. 엔티티 생성일자(created_at)
    """
    try:
        result = await notice_crud.get_multi(
            request=request,
            skip=skip,
            limit=limit,
            sort=sort,
            type="filter",
            field="notice_type",
            value=value.value,
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
    path="",
    responses=create_response,
    dependencies=[Depends(admin_crud.auth_user)],
)
async def create_notice(request: Request) -> JSONResponse:
    """
    공지 생성(POST) 엔드포인트
    이때 헤더는 application/form-data로 보낸다.

    아래는 선택적으로 전달할 수 있는 파일 폼 데이터(Form Data)
    1. files[0]

    이때 다수의 파일을 보낼 경우 아래와 같이 넘버링하여 보낸다.
    1. files[0]
    2. files[1]

    아래 세 개는 필수적으로 전달해야 하는 파일이 아닌 폼 데이터(Form Data)
    1. notice_type
    2. notice_title
    3. notice_content

    이때 전달할 수 있는 공지종류(notice_type)는 아래와 같다.
    1. archive : 자료실
    2. notification : 공지사항
    """
    try:
        form_data = await request.form()
        insert_data = await parse_formdata(
            form_data=form_data,
            schema=CreateNotice,
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
            content={"detail": str(error)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.patch(
    path="/{notice_id}",
    responses=update_response,
    dependencies=[Depends(admin_crud.auth_user)],
)
async def update_notice_partialy(
    request: Request, notice_id: str
) -> JSONResponse:
    """
    공지 수정(PATCH) 엔드포인트

    아래 한 개는 필수적으로 전달해야 하는 패스 파라미터(Path Parameter)
    1. _id

    이때 헤더는 application/form-data로 보낸다.

    아래는 선택적으로 전달할 수 있는 파일 폼 데이터(Form Data)
    1. files[0]

    이때 다수의 파일을 보낼 경우 아래와 같이 넘버링하여 보낸다.
    1. files[0]
    2. files[1]

    아래 세 개는 필수적으로 전달해야 하는 파일이 아닌 폼 데이터(Form Data)
    1. notice_type
    2. notice_title
    3. notice_content

    이때 전달할 수 있는 공지종류(notice_type)는 아래와 같다.
    1. archive : 자료실
    2. notification : 공지사항
    """
    try:
        form_data = await request.form()
        update_data = await parse_formdata(
            form_data=form_data,
            schema=UpdateNotice,
            collection_name="notices",
        )

        if await notice_crud.update(
            request=request, id=notice_id, update_data=update_data
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
    path="/{notice_id}",
    responses=delete_response,
    dependencies=[Depends(admin_crud.auth_user)],
)
async def delete_notice(request: Request, notice_id: str) -> JSONResponse:
    """
    공지 삭제(DELETE) 엔드포인트

    아래 한 개는 필수적으로 전달해야 하는 패스 파라미터(Path Parameter)
    1. _id
    """
    try:
        if await notice_crud.delete(request=request, id=notice_id):
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
