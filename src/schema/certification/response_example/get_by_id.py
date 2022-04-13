from src.schema.response import ErrorResponseModel, GetResponseModel

get_certification_response = {
    "200": {
    "model": GetResponseModel,
    "description": "성공",
    "content": {"application/json": {
        "example": {
            "data": [
                {
                    "_id": "624db4e86a6b5d4406086417",
                    "created_at": "2022-04-07T01:00:12.819961+09:00",
                    "updated_at": "null",
                    "deleted_at": "null",
                    "certification_type": "test-results",
                    "certification_title": "버블 댐퍼",
                    "certification_content": "null",
                    "certification_date": "2012. 09. 04 - 2012. 09. 21",
                    "certification_organization": "한국기계전자시험연구원",
                    "certification_images": [
                        {
                            "name": "",
                            "url": "",
                            "type": "image"
                        },
                        {
                            "name": "",
                            "url": "",
                            "type": "image"
                        }
                    ]
                }
            ]
        }
    }}},
    "400": {
        "model": ErrorResponseModel,
        "description": "유효하지 않은 형태의 ObjectId 요청",
        "content": {
            "application/json": {
                "example": {"detail": "'62541f20ac27' is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string"}
            }
        },
    },
    "404": {
        "model": GetResponseModel,
        "description": "존재하지 않는 엔티티",
        "content": {"application/json": {"example": {"data": []}}},
    },
}
