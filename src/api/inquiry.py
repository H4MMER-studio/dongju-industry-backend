from bson.objectid import InvalidId
from fastapi import APIRouter, Query, Request, status
from fastapi.responses import JSONResponse

from src.crud import inquiry_crud
from src.schema import CreateInquiry

SINGLE_PREFIX = "/inquiry"
PLURAL_PREFIX = "/inquiries"

router = APIRouter()


@router.get(SINGLE_PREFIX + "/{inquiry_id}")
async def get_inquiry(request: Request, inquiry_id: str):
    """
    고객문의 조회(GET) 엔드포인트

    아래 한 개는 필수적으로 전달해야 하는 패스 파라미터(Path Parameter)
    1. _id
    """
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
            content={"detail": str(error)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.get(PLURAL_PREFIX)
async def get_inquries(
    request: Request,
    skip: int = Query(default=0, description="페이지네이션 시작 값", example=1),
    limit: int = Query(default=0, description="페이지네이션 종료 값", example=30),
    sort: list[str] = Query(
        default=["created-at desc"],
        description="정렬 기준",
        example=["created-at desc"],
    ),
) -> JSONResponse:
    """
    고객문의 다량 조회(GET) 엔드포인트

    아래 세 개는 선택적으로 전달할 수 있는 쿼리 파라미터(Query Parameter)
    1. sort
    2. skip
    3. limit

    이때 기본적으로 아래 순서를 기준으로 내림차순 정렬하여 결과를 반환한다.
    1. 엔티티 생성일자(created_at)
    """
    try:
        if result := await inquiry_crud.get_multi(
            request=request, skip=skip, limit=limit, sort=sort
        ):
            return JSONResponse(
                content={"data": result["data"], "size": result["data_size"]},
                status_code=status.HTTP_200_OK,
            )

        else:
            return JSONResponse(
                content={"data": []}, status_code=status.HTTP_404_NOT_FOUND
            )

    except Exception as error:
        return JSONResponse(
            content={"detail": str(error)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.post(SINGLE_PREFIX)
async def create_inquiry(
    request: Request, insert_data: CreateInquiry
) -> JSONResponse:
    """
    고객문의 생성(POST) 엔드포인트

    아래는 필수적으로 전달해야 하는 바디 파라미터(Body Parameter)
    1. inquiry_title
    2. inquiry_content
    3. inquiry_content
    4. inquiry_person_name
    5. inquiry_company_name
    6. inquiry_phone_number
    7. inquiry_email
    8. inquiry_type
    9. inquiry_product_type

    이때 고객문의종류(inquiry_type)는 아래와 같다.
    1. estimate : 견적문의
    2. after-service : A/S문의
    3. etc : 그 외 문의

    이때 제품종류(inquiry_product_type)는 아래와 같다.
    1. air-conditioner
    2. freeze-protection-damper-coil
    3. exhaust-unit
    4. bubble-damper
    5. fully-sealed-door
    """
    try:
        await inquiry_crud.create(request=request, insert_data=insert_data)

        return JSONResponse(
            content={"detail": "Success"}, status_code=status.HTTP_200_OK
        )

    except Exception as error:
        return JSONResponse(
            content={"detail": str(error)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.post(SINGLE_PREFIX)
async def reply_inquiry(
    request: Request,
) -> JSONResponse:
    """
    고객문의 답변(POST) 엔드포인트


    """
    try:
        return

    except Exception as error:
        return JSONResponse(
            content={"detail": str(error)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
