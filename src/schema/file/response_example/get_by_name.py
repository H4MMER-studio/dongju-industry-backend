from src.schema.response import GetResponseModel

file_download_response = {
    "200": {
        "model": GetResponseModel,
        "description": "성공 : 이때 전달되는 파일은 바이너리(Binary) 데이터다.",
        "content": {
            "application/pdf": {
                "example": "b'123456789'"
            }
        }
    },
    "404": {
        "model": GetResponseModel,
        "description": "존재하지 않는 엔티티",
        "content": {
            "application/json": {
                "example": {"data": "[]"}
            }
        },
    },
}
