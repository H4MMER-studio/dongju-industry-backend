from src.schema.response_base import AlterResponseModel

create_response = {
    "200": {
        "model": AlterResponseModel,
        "description": "성공",
        "content": {
            "application/json": {
                "example": {"detail": "Success"}
            }
        },
    }
}
