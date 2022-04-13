from src.schema.response import ErrorResponseModel
from src.schema.response_example.create import create_response

create_inquiry_response = create_response

create_inquiry_response["422"] = {
    "model": ErrorResponseModel,
    "description": "유효하지 않은 파라미터 사용 : 이때 그 파라미터의 종류와 이름을 반환한다.",
    "content": {
        "application/json": {
            "example": {
                "detail": [
                    {
                        "loc": ["body", "inquiry_product_type"],
                        "msg": "value is not a valid enumeration member; permitted: 'air-conditioner', 'freeze-protection-damper-coil', 'exhaust-unit', 'bubble-damper', 'fully-sealed-door'",
                        "type": "type_error.enum",
                        "ctx": {
                            "enum_values": [
                                "air-conditioner",
                                "freeze-protection-damper-coil",
                                "exhaust-unit",
                                "bubble-damper",
                                "fully-sealed-door",
                            ]
                        },
                    }
                ]
            }
        }
    },
}
