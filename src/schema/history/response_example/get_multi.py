from src.schema.response_base import GetResponseModel

get_histories_response = {
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
                                    "history_year": 2021,
                                    "history_month": 1,
                                    "history_content": "안양 영업사무소 설립",
                                },
                                {
                                    "_id": "624db4d66a6b5d4406086415",
                                    "created_at": "2022-04-07",
                                    "updated_at": "null",
                                    "deleted_at": "null",
                                    "history_year": 2021,
                                    "history_month": 1,
                                    "history_content": "현 공동대표이사 취임 (이왕주, 전축식 대표이사)",
                                },
                                {
                                    "_id": "624db4df6a6b5d4406086416",
                                    "created_at": "2022-04-07",
                                    "updated_at": "null",
                                    "deleted_at": "null",
                                    "history_year": 1991,
                                    "history_month": 5,
                                    "history_content": "동주산업 설립 (서울, 시흥 소재)",
                                }
                            ],
                            "size": 20,
                        },
                    },
                    "Not Found": {
                        "summary": "데이터베이스에 엔티티가 존재하지 않는 경우",
                        "value": {"data": []}
                    }
                }
            }
        },
    },
}
