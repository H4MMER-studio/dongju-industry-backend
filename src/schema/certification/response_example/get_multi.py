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
                "certification_type": "test-result",
                "certification_title": "버블 댐퍼",
                "certification_content": "null",
                "certification_start_date": "2021-02-02",
                "certification_end_date": "null",
                "certification_organization": "한국기계전자시험연구원",
                "certification_images": [
                    {
                        "name": "",
                        "url": "",
                    },
                    {
                        "name": "",
                        "url": "",
                    }
                ]
            },
            {
                "_id": "624db4e86a6b5d4406086417",
                "created_at": "2022-04-07T01:00:12.819961+09:00",
                "updated_at": "null",
                "deleted_at": "null",
                "certification_type": "test-result",
                "certification_title": "배기 유니트",
                "certification_content": "null",
                "certification_start_date": "2015-03-24",
                "certification_end_date": "2015-03-26",
                "certification_organization": "(주)한국필터시험원",
                "certification_images": [
                    {
                        "name": "",
                        "url": "",
                    }
                ]
            },
            {
                "_id": "624db4e86a6b5d4406086417",
                "created_at": "2022-04-07T01:00:12.819961+09:00",
                "updated_at": "null",
                "deleted_at": "null",
                "certification_type": "test-result",
                "certification_title": "배기 유니트",
                "certification_content": "null",
                "certification_start_date": "2015-01-20",
                "certification_end_date": "2015-02-26",
                "certification_organization": "(주)한국필터시험원",
                "certification_images": [
                    {
                        "name": "",
                        "url": "",
                    },
                    {
                        "name": "",
                        "url": "",
                    }
                ]
            },
        ],
        "size": 4
        }}},
    },
    "404": {
        "model": GetResponseModel,
        "description": "존재하지 않는 엔티티",
        "content": {"application/json": {"example": {"detail": "not found"}}},
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
                        "msg": "value is not a valid enumeration member; permitted: 'license', 'core-certification', 'patent', 'test-result'",
                        "type": "type_error.enum",
                        "ctx": {
                            "enum_values": [
                                    "license",
                                    "core-certification",
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
