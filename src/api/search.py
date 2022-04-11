from fastapi import APIRouter, Body, Query, Request, status
from fastapi.responses import JSONResponse

from src.crud import CRUDBase

SINGLE_PREFIX = "/search"

router = APIRouter(prefix=SINGLE_PREFIX)


@router.get("/{collection}")
async def search(
    request: Request,
    collection: str,
    skip: int = Query(default=0),
    limit: int = Query(default=0),
    sort: list[str] = Query(default=None),
    filter: dict = Body(...),
) -> JSONResponse:
    try:
        search_crud = CRUDBase(collection=collection)

        if result := await search_crud.get_multi(
            request=request, skip=skip, limit=limit, sort=sort, filter=filter
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
