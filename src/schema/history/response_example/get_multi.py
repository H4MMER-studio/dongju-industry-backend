from src.schema.response import GetResponseModel

get_histories_response = {
    "200": {
    "model": GetResponseModel,
    "description": "성공",
    "content": {"application/json": {"example": {"data": [
            {
                "_id": "624db4e86a6b5d4406086417",
                "created_at": "2022-04-07T01:00:12.819961+09:00",
                "updated_at": "null",
                "deleted_at": "null",
                "history_year": 2021,
                "history_month": 1,
                "history_content": "안양 영업사무소 설립",
            },
            {
                "_id": "624db4d66a6b5d4406086415",
                "created_at": "2022-04-07T01:00:12.819961+09:00",
                "updated_at": "null",
                "deleted_at": "null",
                "history_year": 2021,
                "history_month": 1,
                "history_content": "현 공동대표이사 취임 (이왕주, 전축식 대표이사)",
            },
            {
                "_id": "624db4df6a6b5d4406086416",
                "created_at": "2022-04-07T01:00:12.819961+09:00",
                "updated_at": "null",
                "deleted_at": "null",
                "history_year": 1991,
                "history_month": 5,
                "history_content": "동주산업 설립 (서울, 시흥 소재)",
            }
        ],
        "size": 20,
        }}},
    },
    "404": {
        "model": GetResponseModel,
        "description": "존재하지 않는 엔티티",
        "content": {"application/json": {"example": {"detail": "not found"}}},
    },
}
