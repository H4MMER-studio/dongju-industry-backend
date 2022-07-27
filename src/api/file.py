from botocore.exceptions import ClientError
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse, Response

from src.schema import file_download_response
from src.util import file_crud

SINGLE_PREFIX = "/file"

router = APIRouter(prefix=SINGLE_PREFIX)


@router.get(path="/{file_name}", responses=file_download_response)
async def download_file(file_name: str) -> Response | JSONResponse:
    """
    파일 다운로드(GET) 엔드포인트

    아래 한 개는 필수적으로 전달해야하는 패스 파라미터(Path Parameter)
    1. file_name
    """
    try:
        file = await file_crud.download(file_name)

        return Response(content=file, status_code=status.HTTP_200_OK)

    except ClientError as aws_error:
        if aws_error.response["Error"]["Code"] == "NoSuchKey":
            return JSONResponse(
                content={"detail": "not found"},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        else:
            return JSONResponse(
                content={"detail": aws_error},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    except Exception as error:
        return JSONResponse(
            content={"detail": str(error)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
