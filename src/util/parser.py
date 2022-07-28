import re
from datetime import datetime, timedelta, timezone
from typing import TypeVar

from fastapi import UploadFile
from pydantic import BaseModel, ValidationError
from starlette.datastructures import FormData

from src.util.file import file_crud

Schema = TypeVar("Schema", bound=BaseModel)


async def get_datetime() -> datetime:
    return datetime.now(tz=timezone(offset=timedelta(hours=9)))


async def datetime_to_str(datetime: datetime) -> str:
    return datetime.strftime("%Y-%m-%d")


async def str_to_datetime(date_string: str, format=str) -> datetime:
    return datetime.strptime(date_string, format)


async def parse_formdata(
    form_data: FormData, schema: Schema, collection_name: str
) -> Schema:
    if not form_data:
        raise ValidationError

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

        uploaded_files = await file_crud.upload(files=files)

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


async def create_decompsed_korean_field(schema: Schema, fields):
    schema_dict: dict = schema.dict()

    for field in fields:
        for key, value in schema_dict.items():
            if field == key:
                schema_dict[key] = {
                    "composed": value,
                    "decomposed": await decompose_korean(input=value),
                }

    return schema_dict


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
