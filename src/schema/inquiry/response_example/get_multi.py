from src.schema.response_base import GetResponseModel

get_inquiries_response = {
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
                                    {
                                        "_id": "6256d2a5ff5d327127a21319",
                                        "created_at": "2022-04-13",
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
                                        "inquiry_resolved_status": False
                                    },
                                    {
                                        "_id": "6256d2a5ff5d327127a21319",
                                        "created_at": "2022-04-13",
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
