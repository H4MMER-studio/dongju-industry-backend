from src.schema.response_base import ErrorResponseModel, GetResponseModel

get_certifications_response = {
    "200": {
        "model": GetResponseModel,
        "description": "엔티티 조회",
        "content": {
            "application/json": {
                "examples": {
                    "Success": {
                        "summary": "데이터베이스에 엔티티가 존재하는 경우",
                        "value": {
                            "data": [
                                {
                                    "_id": "624db4e86a6b5d4406086417",
                                    "created_at": "2022-04-07",
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
                                            "key": "",
                                        },
                                        {
                                            "name": "",
                                            "url": "",
                                            "key": "",
                                        }
                                    ]
                                },
                                {
                                    "_id": "624db4e86a6b5d4406086417",
                                    "created_at": "2022-04-07",
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
                                            "key": "",
                                        }
                                    ]
                                },
                                {
                                    "_id": "624db4e86a6b5d4406086417",
                                    "created_at": "2022-04-07",
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
                                            "key": "",
                                        },
                                        {
                                            "name": "",
                                            "url": "",
                                            "key": "",
                                        }
                                    ]
                                },
                            ],
                            "size": 4
                        }
                    },
                    "Not Found": {
                        "summary": "데이터베이스에 엔티티가 존재하지 않는 경우",
                        "value": {"data": []}
                    }
                }
            },
        },
    },
    "422": {
        "model": ErrorResponseModel,
        "description": "유효하지 않은 파라미터 사용 : 이때 그 파라미터의 종류와 이름을 반환한다.",
        "content": {
            "application/json": {
                "example": {
                    "detail": [{
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
                    }]
                }
            }
        },
    },
}
