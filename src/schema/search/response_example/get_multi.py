from src.schema.response import ErrorResponseModel, GetResponseModel

get_search_response = {
    "200": {
        "model": GetResponseModel,
        "description": "성공",
        "content": {
            "application/json": {
                "example":
                {
                    "data": [
                        {
                            "_id": "625d78ec45a235c40e92f3ff",
                            "created_at": "2022-04-18T23:42:24.677289+09:00",
                            "updated_at": "null",
                            "deleted_at": "null",
                            "inquiry_type": "estimate",
                            "inquiry_title": "안녕하세요. 댐퍼 코일 견적 관련 문의입니다.",
                            "inquiry_email": "H4MMER@naver.com",
                            "inquiry_person_name": "김해머",
                            "inquiry_company_name": "해머스튜디오",
                            "inquiry_product_type": "freeze-protection-damper-coil",
                            "inquiry_phone_number": "010-1234-5678",
                            "inquiry_content": "안녕하세요. 댐퍼 코일 견적을 좀 여쭤보고 싶은데 저희 회사 실험실에 사용할 예정입니다.",
                            "inquiry_resolved_status": True
                        },
                        {
                            "_id": "625d790d45a235c40e92f400",
                            "created_at": "2022-04-18T23:42:24.677289+09:00",
                            "updated_at": "null",
                            "deleted_at": "null",
                            "inquiry_type": "estimate",
                            "inquiry_title": "안녕하세요. 댐퍼 코일 견적 관련 문의입니다.",
                            "inquiry_email": "H4MMER@naver.com",
                            "inquiry_person_name": "sdfgas",
                            "inquiry_company_name": "해머스튜디오",
                            "inquiry_product_type": "freeze-protection-damper-coil",
                            "inquiry_phone_number": "010-1234-5678",
                            "inquiry_content": "안녕하세요. 댐퍼 코일 견적을 좀 여쭤보고 싶은데 저희 회사 실험실에 사용할 예정입니다.",
                            "inquiry_resolved_status": True
                        },
                        {
                            "_id": "625d792b45a235c40e92f401",
                            "created_at": "2022-04-18T23:42:24.677289+09:00",
                            "updated_at": "null",
                            "deleted_at": "null",
                            "inquiry_type": "estimate",
                            "inquiry_title": "안녕하세요. 댐퍼 코일 견적 관련 문의입니다.",
                            "inquiry_email": "H4MMER@naver.com",
                            "inquiry_person_name": "asdf",
                            "inquiry_company_name": "해머스튜디오",
                            "inquiry_product_type": "freeze-protection-damper-coil",
                            "inquiry_phone_number": "010-1234-5678",
                            "inquiry_content": "안녕하세요. 댐퍼 코일 견적을 좀 여쭤보고 싶은데 저희 회사 실험실에 사용할 예정입니다.",
                            "inquiry_resolved_status": True
                        }
                    ],
                    "size": 8
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
                            "msg": "value is not a valid enumeration member; permitted: 'deliveries', 'inquiries'",
                            "type": "type_error.enum",
                            "ctx": {
                                "enum_values": ["deliveries", "inquiries"]
                            },
                        }
                    ]
                }
            }
        },
    },
}
