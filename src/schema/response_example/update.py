from src.schema.response_base import AlterResponseModel, ErrorResponseModel

update_response = {
    "200": {
        "model": AlterResponseModel,
        "description": "앤티티 수정",
        "content": {
            "application/json": {
                "examples": {
                    "Success": {
                        "summary": "데이터베이스에 엔티티가 존재하는 경우",
                        "value": {"detail": "Success"},
                    },
                    "Not Found": {
                        "summary": "데이터베이스에 엔티티가 존재하지 않는 경우",
                        "value": {"data": []},
                    }
                }
            }
        },
    },
    "400": {
        "model": ErrorResponseModel,
        "description": "유효하지 않은 형태의 ObjectId 요청",
        "content": {
            "application/json": {
                "example": {
                    "detail": "'62541f20ac27' is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string"
                }
            }
        },
    },
}
