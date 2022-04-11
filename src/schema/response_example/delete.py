from src.schema.response import (
    AlterResponseModel,
    ErrorResponseModel,
    GetResponseModel,
)

delete_response = {
    "200": {
        "model": AlterResponseModel,
        "description": "성공",
        "content": {"application/json": {"example": {"detail": "Success"}}},
    },
    "400": {
        "model": ErrorResponseModel,
        "description": "유효하지 않은 형태의 ObjectId 요청",
        "content": {
            "application/json": {
                "example": {"detail": "ObjectId 1234 Invalid"}
            }
        },
    },
    "404": {
        "model": GetResponseModel,
        "description": "존재하지 않는 엔티티",
        "content": {"application/json": {"example": {"data": []}}},
    },
}
