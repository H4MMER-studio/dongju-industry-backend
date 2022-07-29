from bson.objectid import InvalidId
from fastapi import APIRouter, Depends, Query, Request, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from src.crud import admin_crud, certification_crud
from src.schema import (
    CertificationType,
    CreateCertification,
    UpdateCertification,
    create_response,
    delete_response,
    get_certification_response,
    get_certifications_response,
    update_response,
)
from src.util import parse_formdata

SINGLE_PREFIX = "/certification"

router = APIRouter(prefix=SINGLE_PREFIX)


@router.get(path="/{certification_id}", responses=get_certification_response)
async def get_certification(
    request: Request, certification_id: str
) -> JSONResponse:
    """
    인증 개별 조회(GET) 엔드포인트

    아래 한 개는 필수적으로 전달해야 하는 패스 파라미터(Path Parameter)
    1. _id
    """
    try:
        if result := await certification_crud.get_one(
            request=request,
            id=certification_id,
        ):
            return JSONResponse(
                content={"data": result}, status_code=status.HTTP_200_OK
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


@router.get(path="s", responses=get_certifications_response)
async def get_certifications(
    request: Request,
    value: CertificationType
    | None = Query(default=None, description="인증 종류", example="test-result"),
    skip: int = Query(default=0, description="페이지네이션 시작 값", example=1),
    limit: int = Query(default=0, desciption="페이지네이션 종료 값", example=30),
    sort: list[str] = Query(
        default=["certification-start-date asc", "certification-title asc"],
        description="정렬 기준",
        example=["certification-start-date asc", "certification-title asc"],
    ),
) -> JSONResponse:
    """
    인증 종류별 다량 조회(GET) 엔드포인트

    아래 한 개는 선택적으로 전달해야 하는 쿼리 파라미터(Query Parameter)
    1. value

    이때 그 값으로 인증종류(certification_type)를 전달한다.
    전달할 수 있는 인증종류는 아래와 같다.
    1. license : 등록증
    2. patent : 특허증
    3. test-result : 시험 성적서
    4. core-certification : 주요 인증

    만약 따로 value 쿼리 파라미터를 전달하지 않으면 전체 인증종류에 대한 결괏값을 반환한다.

    아래 세 개는 선택적으로 전달할 수 있는 쿼리 파라미터(Query Parameter)
    1. sort
    2. skip
    3. limit

    이때 기본적으로 아래 기준으로 오름차순 정렬하여 결과를 반환한다.
    1. 인증일자(certification_date)
    """
    try:
        if value:
            field = "certification_type"
            value = value.value

        else:
            field = None

        result = await certification_crud.get_multi(
            request=request,
            skip=skip,
            limit=limit,
            sort=sort,
            type="filter",
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
                content={"data": []},
                status_code=status.HTTP_200_OK,
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
async def create_certification(request: Request) -> JSONResponse:
    """
    인증 생성(POST) 엔드포인트
    이때 헤더는 application/form-data로 보낸다.

    아래는 필수적으로 전달해야 하는 파일 폼 데이터(Form Data)
    1. files[0]

    이때 다수의 파일을 보낼 경우 아래와 같이 넘버링하여 보낸다.
    1. files[0]
    2. files[1]

    아래 두 개는 필수적으로 전달해야 하는 파일이 아닌 폼 데이터(Form Data)
    1. certification_type
    2. certification_title

    이때 전달할 수 있는 인증종류(certification_type)는 아래와 같다.
    1. license : 등록증
    2. patent : 특허증
    3. test-result : 시험성적서
    4. core-certification : 주요 인증

    아래 두 개는 선택적으로 전달할 수 있는 파일이 아닌 폼 데이터(Form Data)
    1. certification_content
    2. certification_start_date
    3. certification_end_date
    4. certification_organization

    이때 일자를 전달하는 형식은 아래와 같다.
    - YYYY-mm-dd
    """
    try:
        form_data = await request.form()
        insert_data = await parse_formdata(
            form_data=form_data,
            schema=CreateCertification,
            collection_name="certification",
        )

        if await certification_crud.create(
            request=request, insert_data=insert_data
        ):
            return JSONResponse(
                content={"detail": "Success"}, status_code=status.HTTP_200_OK
            )

        else:
            return JSONResponse(
                content={"datail": "Database Error"},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    except ValidationError as validation_error:
        return JSONResponse(
            content={"detail": validation_error.errors()},
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    except ValueError as value_error:
        return JSONResponse(
            content={"detail": str(value_error)},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    except Exception as error:
        return JSONResponse(
            content={"detail": str(error)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.patch(
    path="/{certification_id}",
    responses=update_response,
    dependencies=[Depends(admin_crud.auth_user)],
)
async def update_certification_partialy(
    request: Request, certification_id: str
) -> JSONResponse:
    """
    인증 수정(PATCH) 엔드포인트
    이때 헤더는 application/form-data로 보낸다.

    아래 한 개는 필수적으로 전달해야 하는 패스 파라미터(Path Parameter)
    1. _id

    아래 한 개는 선택적으로으로 전달할 수 있는 파일 폼 데이터(Form Data)
    1. files[0]

    이때 다수의 파일을 보낼 경우 아래와 같이 넘버링하여 보낸다.
    1. files[0]
    2. files[1]

    아래는 선택적으로 전달할 수 있는 파일이 아닌 폼 데이터(Form Data)
    1. certification_type
    2. certification_title
    3. certification_content
    4. certification_start_date
    5. certification_end_date
    6. certification_organization

    이때 전달할 수 있는 인증종류(certification_type)는 아래와 같다.
    1. license : 등록증
    2. patent : 특허증
    3. test-result : 시험성적서
    4. core-certification : 주요 인증

    이때 일자를 전달하는 형식은 아래와 같다.
    - YYYY-mm-dd
    """
    try:
        form_data = await request.form()
        update_data = await parse_formdata(
            form_data=form_data,
            schema=UpdateCertification,
            collection_name="certification",
        )

        if await certification_crud.update(
            request=request, id=certification_id, update_data=update_data
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
    path="/{certification_id}",
    responses=delete_response,
    dependencies=[Depends(admin_crud.auth_user)],
)
async def delete_certification(
    request: Request, certification_id: str
) -> JSONResponse:
    """
    인증 삭제(DELETE) 엔드포인트

    아래 한 개는 필수적으로 전달해야 하는 패스 파라미터(Path Parameter)
    1. _id
    """
    try:
        result = await certification_crud.delete(
            request=request, id=certification_id
        )
        if result["status"]:
            return JSONResponse(
                content={"detail": "Success"}, status_code=status.HTTP_200_OK
            )

        elif result["detail"] == "Not Found":
            return JSONResponse(
                content={"data": []}, status_code=status.HTTP_200_OK
            )

        else:
            return JSONResponse(
                content={"detail": result["detail"]},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
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
