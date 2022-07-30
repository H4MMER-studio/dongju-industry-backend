from src.schema.response_base import GetResponseModel

get_deliveries_response = {
    "200": {
        "model": GetResponseModel,
        "description": "엔티티 ",
        "content": {
            "application/json": {
                "examples": {
                    "Success": {
                        "summary": "데이터베이스에 엔티티가 존재하는 경우",
                        "value": {
                            "data": [
                                {
                                    "_id": "62e50c2668850ef94ca02694",
                                    "delivery_supplier": "(주)웃샘",
                                    "delivery_product": "헤파유닛",
                                    "delivery_amount": 22,
                                    "delivery_reference": "서울대학교",
                                    "updated_at": "null",
                                    "deleted_at": "null",
                                    "created_at": "2022-07-30",
                                    "delivery_date": "2014-11"
                                },
                                {
                                    "_id": "62e50c2668850ef94ca02696",
                                    "delivery_supplier": "(주)세진에스.이",
                                    "delivery_product": "동파방지댐퍼코일",
                                    "delivery_amount": 151,
                                    "delivery_reference": "null",
                                    "updated_at": "null",
                                    "deleted_at": "null",
                                    "created_at": "2022-07-30",
                                    "delivery_date": "2014"
                                },
                            ],
                            "size": 20,
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
}
