from fastapi import APIRouter, Path, Query, Request, status
from fastapi.responses import JSONResponse

from src.crud import CRUDBase
from src.schema import SearchType, get_search_response

SINGLE_PREFIX = "/search"

router = APIRouter(prefix=SINGLE_PREFIX)


@router.get("/{collection}", responses=get_search_response)
async def search(
    request: Request,
    collection: SearchType = Path(
        ..., description="검색 종류", example="inquiries"
    ),
    field: str = Query(..., description="", example=""),
    value: str = Query(..., description="", example=""),
    skip: int
    | None = Query(default=None, description="페이지네이션 시작 값", example=0),
    limit: int
    | None = Query(default=None, description="페이지네이션 종료 값", example=30),
    sort: list[str] = Query(
        default=["created-at asc"],
        description="정렬 기준",
        example=["created-at asc"],
    ),
) -> JSONResponse:
    """
    검색 종류별 다량 조회(GET) 엔드포인트

    아래 한 개는 필수적으로 전달해야 하는 패스 파라미터(Path Parameter)
    1. collection

    이때 그 값으로 검색 대상이 되는 컬렉션 종류를 전달한다.
    전달할 수 있는 컬렉션 종류는 아래와 같다.
    1. deliveries : 납품실적
    2. inquiries : 고객문의

    아래 두 개는 필수적으로 전달해야 하는 쿼리 파라미터(Query Parameter)
    1. field
    2. value

    아래 세 개는 선택적으로 전달할 수 있는 쿼리 파라미터(Query Parameter)
    1. sort
    2. skip
    3. limit

    이때 기본적으로 아래 기준으로 오름차순 정렬하여 결과를 반환한다.
    1. 엔티티 생성일자(created_at)
    """
    try:
        search_crud = CRUDBase(collection=collection)

        if result := await search_crud.get_multi(
            request=request,
            skip=skip,
            limit=limit,
            sort=sort,
            filter_field=field,
            filter_value=value,
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
            content={"detail": error},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
