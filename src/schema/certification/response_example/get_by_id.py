from src.schema.response_base import ErrorResponseModel, GetResponseModel

get_certification_response = {
    "200": {
        "model": GetResponseModel,
        "description": "엔티티 조회",
        "content": {
            "application/json": {
                "examples": {
                    "Success": {
                        "summary": "데이터베이스에 엔티티가 존재하는 경우",
                        "value": {
                            "data": {
                                "_id": "624db4e86a6b5d4406086417",
                                "created_at": "2022-04-07",
                                "updated_at": "null",
                                "deleted_at": "null",
                                "certification_type": "test-results",
                                "certification_title": "버블 댐퍼",
                                "certification_content": "null",
                                "certification_start_date": "2012. 09. 04",
                                "certification_end_date": "2012. 09. 21",
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
                                    },
                                ],
                            }
                        }
                    },
                    "Not Found": {
                        "summary": "데이터베이스에 엔티티가 존재하지 않는 경우",
                        "value": {"data": []}
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
    }
}
