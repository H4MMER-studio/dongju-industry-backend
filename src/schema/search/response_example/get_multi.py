from src.schema.response import ErrorResponseModel, GetResponseModel

get_search_response = {
    "200": {
        "model": GetResponseModel,
        "description": "성공",
        "content": {
            "application/json": {
                "example": {
                    "data": [
                        {
                            "_id": "62542205f3dfe27c2294b6fc",
                            "created_at": "2022-04-11T21:40:24.055982+09:00",
                            "updated_at": "null",
                            "deleted_at": "null",
                            "delivery_supplier": "(주)웃샘",
                            "delivery_product": "AHU 외",
                            "delivery_amount": 1,
                            "delivery_year": 2012,
                            "delivery_month": 2,
                            "delivery_reference": "용인SD",
                        },
                        {
                            "_id": "6254224bf3dfe27c2294b6fe",
                            "created_at": "2022-04-11T21:40:24.055982+09:00",
                            "updated_at": "null",
                            "deleted_at": "null",
                            "delivery_supplier": "(주)웃샘",
                            "delivery_product": "배기 UNIT",
                            "delivery_amount": 0,
                            "delivery_year": 2012,
                            "delivery_month": 3,
                            "delivery_reference": "대전",
                        },
                        {
                            "_id": "62542257f3dfe27c2294b6ff",
                            "created_at": "2022-04-11T21:40:24.055982+09:00",
                            "updated_at": "null",
                            "deleted_at": "null",
                            "delivery_supplier": "(주)웃샘",
                            "delivery_product": "AHU 외",
                            "delivery_amount": 1,
                            "delivery_year": 2012,
                            "delivery_month": 4,
                            "delivery_reference": "고려대",
                        },
                    ]
                }
            }
        },
    },
    "404": {
        "model": GetResponseModel,
        "description": "존재하지 않는 엔티티",
        "content": {"application/json": {"example": {"data": []}}},
    },
    "422": {
        "model": ErrorResponseModel,
        "description": "유효하지 않은 파라미터 사용 : 이때 그 파라미터의 종류와 이름을 반환한다.",
        "content": {
            "application/json": {
                "example": {
                    "detail": [
                        {
                            "loc": ["query", "value"],
                            "msg": "value is not a valid enumeration member; permitted: 'deliveries', 'inquiries'",
                            "type": "type_error.enum",
                            "ctx": {
                                "enum_values": ["deliveries", "inquiries"]
                            },
                        }
                    ]
                }
            }
        },
    },
}
