from bson.objectid import InvalidId
from fastapi import APIRouter, Query, Request, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from src.crud import certification_crud
from src.schema import (
    CertificationType,
    CreateCertification,
    UpdateCertification,
)
from src.util import parse_formdata

SINGLE_PREFIX = "/certification"

router = APIRouter(prefix=SINGLE_PREFIX)


@router.get("/{certification_id}")
async def get_certification(
    request: Request, certification_id: str
) -> JSONResponse:
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


@router.get("s/{certification_type}")
async def get_certifications(
    request: Request,
    skip: int = Query(default=0),
    limit: int = Query(default=0),
    filter: CertificationType = Query(...),
    sort: list[str] = Query(default=["certification-date asc"]),
) -> JSONResponse:
    try:
        filter_filed = {"certification_type": filter.value}
        if result := await certification_crud.get_multi(
            request=request,
            skip=skip,
            limit=limit,
            sort=sort,
            filter=filter_filed,
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


@router.post("")
async def create_certification(request: Request) -> JSONResponse:
    try:
        form_data = await request.form()
        insert_data = await parse_formdata(
            form_data=form_data,
            create_schema=CreateCertification,
            collection_name="certification",
        )

        await certification_crud.create(
            request=request, insert_data=insert_data
        )

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
            content={"detail": error},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.patch("/{certification_id}")
async def update_certification_partialy(
    request: Request, certification_id: str, update_data: UpdateCertification
) -> JSONResponse:
    try:
        if await certification_crud.update(
            request=request, id=certification_id, update_data=update_data
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


@router.delete("/{certification_id}")
async def delete_certification(
    request: Request, certification_id: str
) -> JSONResponse:
    try:
        if await certification_crud.delete(
            request=request, id=certification_id
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
