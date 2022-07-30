import re
from datetime import datetime, timedelta, timezone
from typing import TypeVar

import numpy as np
import pandas as pd
from fastapi import UploadFile
from pydantic import BaseModel, ValidationError
from starlette.datastructures import FormData

from src.util.file import file_crud

Schema = TypeVar("Schema", bound=BaseModel)


def get_datetime() -> datetime:
    return datetime.now(tz=timezone(offset=timedelta(hours=9)))


def datetime_to_str(datetime: datetime) -> str:
    return datetime.strftime("%Y-%m-%d")


async def parse_excel_file(excel_file: bytes) -> list[dict]:
    insert_data: list[dict] = []
    key_pair: dict[str, str] = {
        "납품처": "delivery_supplier",
        "품명 및 규격": "delivery_product",
        "수량": "delivery_amount",
        "날짜": "delivery_date",
        "비고": "delivery_reference",
    }

    df = pd.ExcelFile(excel_file, engine="openpyxl").parse(index_col=0)
    converted_df = df.replace({np.NaN: None})
    for _, row in converted_df.iterrows():
        temp: dict = {
            "delivery_supplier": None,
            "delivery_product": None,
            "delivery_amount": None,
            "delivery_year": None,
            "delivery_month": None,
            "delivery_reference": None,
            "updated_at": None,
            "deleted_at": None,
        }
        data = row.to_dict()
        for key, value in data.items():
            compared_keys = key_pair.keys()
            if key in compared_keys:
                if (eng_key := key_pair[key]) == "delivery_date":
                    if value:
                        year, month = str(value).split(".")
                        if year:
                            temp["delivery_year"] = int(year)

                        if month:
                            temp["delivery_month"] = int(month)

                else:
                    if value:
                        temp[eng_key] = value

            elif (converted_key := key.replace(" ", "")) in compared_keys:
                if (eng_key := key_pair[converted_key]) == "delivery_date":
                    if value:
                        year, month = str(value).split(".")
                        if year:
                            temp["delivery_year"] = int(year)

                        if month:
                            temp["delivery_month"] = int(month)

                else:
                    if value:
                        temp[eng_key] = value

            else:
                raise ValueError("")

        insert_data.append(temp)

    return insert_data


async def parse_formdata(
    form_data: FormData, schema: Schema, collection_name: str
) -> Schema:
    if not form_data:
        raise ValidationError("FormData Needed")

    else:
        files: list[UploadFile] = []
        fields: dict = {}

        for key, value in form_data.items():
            if re.match(r"(files\[[0-9]+\])", key):
                files.append(value)
            elif re.match(r"[\w]+\_date", key):
                fields[key] = datetime.strptime(value, "%Y-%m-%d")
            else:
                fields[key] = value

        if collection_name == "certification":
            need_converted = True

        else:
            need_converted = False

        uploaded_files = await file_crud.upload(
            files=files, need_converted=need_converted
        )

        for uploaded_file in uploaded_files:
            if (file_type := uploaded_file.pop("type")) == "image":
                file_field = f"{collection_name}_{file_type}s"
            else:
                file_field = f"{collection_name}_files"

            if file_field in fields:
                fields[file_field].append(uploaded_file)
            else:
                fields[file_field] = [uploaded_file]

        insert_data = schema(**fields)

        return insert_data


async def create_decompsed_korean_field(data: dict, fields):
    for field in fields:
        for key, value in data.items():
            if field == key:
                data[key] = {
                    "composed": value,
                    "decomposed": await decompose_korean(input=value),
                }

    return data


async def decompose_korean(input: str) -> str:
    CHOSUNG_LIST: list[str] = [
        "ㄱ",
        "ㄲ",
        "ㄴ",
        "ㄷ",
        "ㄸ",
        "ㄹ",
        "ㅁ",
        "ㅂ",
        "ㅃ",
        "ㅅ",
        "ㅆ",
        "ㅇ",
        "ㅈ",
        "ㅉ",
        "ㅊ",
        "ㅋ",
        "ㅌ",
        "ㅍ",
        "ㅎ",
    ]
    JUNGSUNG_LIST: list[str] = [
        "ㅏ",
        "ㅐ",
        "ㅑ",
        "ㅒ",
        "ㅓ",
        "ㅔ",
        "ㅕ",
        "ㅖ",
        "ㅗ",
        "ㅘ",
        "ㅙ",
        "ㅚ",
        "ㅛ",
        "ㅜ",
        "ㅝ",
        "ㅞ",
        "ㅟ",
        "ㅠ",
        "ㅡ",
        "ㅢ",
        "ㅣ",
    ]
    JONGSUNG_LIST: list[str] = [
        "",
        "ㄱ",
        "ㄲ",
        "ㄳ",
        "ㄴ",
        "ㄵ",
        "ㄶ",
        "ㄷ",
        "ㄹ",
        "ㄺ",
        "ㄻ",
        "ㄼ",
        "ㄽ",
        "ㄾ",
        "ㄿ",
        "ㅀ",
        "ㅁ",
        "ㅂ",
        "ㅄ",
        "ㅅ",
        "ㅆ",
        "ㅇ",
        "ㅈ",
        "ㅊ",
        "ㅋ",
        "ㅌ",
        "ㅍ",
        "ㅎ",
    ]

    result: str = ""
    for word in list(input.strip()):
        if "가" <= word <= "힣":
            first_word: int = (ord(word) - ord("가")) // 588
            middle_word: int = (
                (ord(word) - ord("가")) - (588 * first_word)
            ) // 28
            last_word: int = (
                (ord(word) - ord("가"))
                - (588 * first_word)
                - (28 * middle_word)
            )
            result += "".join(
                [
                    CHOSUNG_LIST[first_word],
                    JUNGSUNG_LIST[middle_word],
                    JONGSUNG_LIST[last_word],
                ]
            )

        else:
            result += word

    return result
