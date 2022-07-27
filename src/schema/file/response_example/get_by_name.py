from src.schema.response_base import GetResponseModel

file_download_response = {
    "200": {
        "model": GetResponseModel,
        "description": "S3에 파일이 존재할 경우 바이너리(Binary) 데이터를 반환하고 존재하지 않을 경우 빈 배열을 반환",
        "content": {
            "application/pdf": {
                "example": "b'123456789...'"
            },
            "application/json": {
                "example": {"data": []}
            }
        }
    }
}
