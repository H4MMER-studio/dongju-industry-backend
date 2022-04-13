from src.schema.response import GetResponseModel

get_deliveries_response = {
    "200": {
        "model": GetResponseModel,
        "description": "성공",
        "content": {"application/json": {"example": {"data": [
        {
            "_id": "62542226f3dfe27c2294b6fd",
            "created_at": "2022-04-11T21:40:24.055982+09:00",
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
            "created_at": "2022-04-11T21:40:24.055982+09:00",
            "updated_at": "null",
            "deleted_at": "null",
            "delivery_supplier": "(주)웃샘",
            "delivery_product": "AHU 외",
            "delivery_amount": 1,
            "delivery_year": 2012,
            "delivery_month": 2,
            "delivery_reference": "용인SD"
        }]}}},
    },
    "404": {
        "model": GetResponseModel,
        "description": "존재하지 않는 엔티티",
        "content": {"application/json": {"example": {"data": []}}},
    },
}
