from src.schema.response_base import GetResponseModel

get_deliveries_response = {
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
                                    "_id": "62542226f3dfe27c2294b6fd",
                                    "created_at": "2022-04-11",
                                    "updated_at": "null",
                                    "deleted_at": "null",
                                    "delivery_supplier": "(주)세진에스.이",
                                    "delivery_product": "COOK FAN",
                                    "delivery_amount": 3,
                                    "delivery_year": 2012,
                                    "delivery_month": 2,
                                    "delivery_reference": "연세대학교"
                                },
                                {
                                    "_id": "62542205f3dfe27c2294b6fc",
                                    "created_at": "2022-04-11",
                                    "updated_at": "null",
                                    "deleted_at": "null",
                                    "delivery_supplier": "(주)웃샘",
                                    "delivery_product": "AHU 외",
                                    "delivery_amount": 1,
                                    "delivery_year": 2012,
                                    "delivery_month": 2,
                                    "delivery_reference": "용인SD"
                                }
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
