from src.schema.response import ErrorResponseModel
from src.schema.response_example.create import create_response

create_history_response = create_response

create_history_response["422"] = {
    "model": ErrorResponseModel,
    "description": "유효하지 않은 파라미터 사용 : 이때 그 파라미터의 종류와 이름을 반환한다.",
    "content": {
        "application/json": {
            "example": {
                "detail": [
                    {
                        "loc": ["body", "history_content"],
                        "msg": "field required",
                        "type": "value_error.missing",
                    },
                    {
                        "loc": ["body", "history_month"],
                        "msg": "field required",
                        "type": "value_error.missing",
                    },
                    {
                        "loc": ["body", "history_year"],
                        "msg": "field required",
                        "type": "value_error.missing",
                    },
                ]
            }
        }
    },
}
