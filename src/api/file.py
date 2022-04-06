from botocore.exceptions import ClientError
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse, Response

from src.crud import file_crud

router = APIRouter()


@router.get("/{file_name}")
async def download_file(file_name: str) -> Response | JSONResponse:
    try:
        file = await file_crud.download(file_name)

        return Response(content=file, status_code=status.HTTP_200_OK)

    except ClientError as aws_error:
        if aws_error.response["Error"]["Code"] == "NoSuchKey":
            return JSONResponse(
                content={"detail": "Not Found"},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        else:
            return JSONResponse(
                content={"detail": aws_error},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    except Exception as error:
        return JSONResponse(
            content={"detail": error},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
