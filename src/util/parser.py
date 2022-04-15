import re
from datetime import datetime
from typing import TypeVar

from fastapi import UploadFile
from pydantic import BaseModel, ValidationError
from starlette.datastructures import FormData

from src.crud import file_crud

Schema = TypeVar("Schema", bound=BaseModel)


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
