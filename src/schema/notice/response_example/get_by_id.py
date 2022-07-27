from src.schema.response_base import ErrorResponseModel, GetResponseModel

get_notice_response = {
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
                                    "_id": "6256c0963d9f91b921c4b581",
                                    "created_at": "2022-04-13",
                                    "updated_at": "null",
                                    "deleted_at": "null",
                                    "notice_type": "archive",
                                    "notice_title": "댐퍼코일 자료입니다.",
                                    "notice_content": "댐퍼코일 관련 자료 올려드립니다. 문의사항은 고객문의 페이지를 이용해주세요.",
                                    "notice_files": [
                                        {
                                            "name": "",
                                            "url": "",
                                            "key": "",
                                        }
                                    ],
                                }
                            }
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
