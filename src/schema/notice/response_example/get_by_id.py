from src.schema.response import ErrorResponseModel, GetResponseModel

get_notice_response = {
    "200": {
        "model": GetResponseModel,
        "description": "성공",
        "content": {
            "application/json": {
                "example": {
                    "data": {
                        "_id": "6256c0963d9f91b921c4b581",
                        "created_at": "2022-04-13T21:20:25.651923+09:00",
                        "updated_at": "null",
                        "deleted_at": "null",
                        "notice_type": "archive",
                        "notice_title": "댐퍼코일 자료입니다.",
                        "notice_content": "댐퍼코일 관련 자료 올려드립니다. 문의사항은 고객문의 페이지를 이용해주세요.",
                        "notice_files": [
                            {"name": "", "url": "",}
                        ],
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
    "404": {
        "model": GetResponseModel,
        "description": "존재하지 않는 엔티티",
        "content": {"application/json": {"example": {"data": []}}},
    },
}
