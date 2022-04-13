from src.schema.response import ErrorResponseModel, GetResponseModel

get_certifications_response = {
    "200": {
    "model": GetResponseModel,
    "description": "성공",
    "content": {"application/json": {"example": {"data": [
            {
                "_id": "624db4e86a6b5d4406086417",
                "created_at": "2022-04-07T01:00:12.819961+09:00",
                "updated_at": "null",
                "deleted_at": "null",
                "certification_type": "test-results",
                "certification_title": "버블 댐퍼",
                "certification_content": "null",
                "certification_date": "2012. 09. 04 - 2012. 09. 21",
                "certification_organization": "한국기계전자시험연구원",
                "certification_images": [
                    {
                        "name": "",
                        "url": "",
                        "type": "image"
                    },
                    {
                        "name": "",
                        "url": "",
                        "type": "image"
                    }
                ]
            },
            {
                "_id": "624db4e86a6b5d4406086417",
                "created_at": "2022-04-07T01:00:12.819961+09:00",
                "updated_at": "null",
                "deleted_at": "null",
                "certification_type": "test",
                "certification_title": "배기 유니트",
                "certification_content": "null",
                "certification_date": "2015. 03. 23",
                "certification_organization": "(주)한국필터시험원",
                "certification_images": [
                    {
                        "name": "",
                        "url": "",
                        "type": "image"
                    }
                ]
            },
            {
                "_id": "624db4e86a6b5d4406086417",
                "created_at": "2022-04-07T01:00:12.819961+09:00",
                "updated_at": "null",
                "deleted_at": "null",
                "certification_type": "test-results",
                "certification_title": "배기 유니트",
                "certification_content": "null",
                "certification_date": "2016. 03. 23",
                "certification_organization": "(주)한국필터시험원",
                "certification_images": [
                    {
                        "name": "",
                        "url": "",
                        "type": "image"
                    },
                    {
                        "name": "",
                        "url": "",
                        "type": "image"
                    }
                ]
            },
        ]}}},
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
                    "detail":[{
                        "loc": [
                            "query",
                            "value"
                        ],
                        "msg": "value is not a valid enumeration member; permitted: 'license', 'certification', 'patent', 'test-result'",
                        "type": "type_error.enum",
                        "ctx": {
                            "enum_values": [
                                    "license",
                                    "certification",
                                    "patent",
                                    "test-result"
                                ]
                            }
                        }
                    ]
                }
            }
        },
    },
}
