from src.schema.response import ErrorResponseModel, GetResponseModel

get_notices_response = {
    "200": {
        "model": GetResponseModel,
        "description": "성공",
        "content": {
            "application/json": {
                "example": {
                    "data": [
                        {
                            "_id": "6256c0963d9f91b921c4b581",
                            "created_at": "2022-04-13T21:20:25.651923+09:00",
                            "updated_at": "null",
                            "deleted_at": "null",
                            "notice_type": "archive",
                            "notice_title": "댐퍼코일 자료입니다.",
                            "notice_content": "댐퍼코일 관련 자료 올려드립니다. 문의사항은 고객문의 페이지를 이용해주세요.",
                            "notice_images": [
                                {"name": "", "url": ""},
                                {"name": "", "url": ""}
                            ],
                            "notice_files": [
                                {"name": "", "url": ""}
                            ],
                        },
                        {
                            "_id": "6256c0963d9f91b921c4b581",
                            "created_at": "2022-04-13T21:20:25.651923+09:00",
                            "updated_at": "null",
                            "deleted_at": "null",
                            "notice_type": "archive",
                            "notice_title": "댐퍼코일 설치사진 및 규격 자료입니다.",
                            "notice_content": "댐퍼코일 실제 설치사진과 각각의 규격 자료 첨부해드립니다. 더 자세한 사항은 고객문의 페이지를 이용해주세요.",
                            "notice_images": "null",
                            "notice_files": [
                                {"name": "", "url": "",},
                                {"name": "", "url": "",},
                            ],
                        },
                    ],
                    "size": 20,
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
                            "msg": "value is not a valid enumeration member; permitted: 'archive', 'notification'",
                            "type": "type_error.enum",
                            "ctx": {
                                "enum_values": [
                                    "archive",
                                    "notification",
                                ]
                            },
                        }
                    ]
                }
            }
        },
    },
}
