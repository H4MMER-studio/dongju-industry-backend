import re
import secrets
from tempfile import TemporaryFile
from urllib import parse

from aioboto3 import Session
from fastapi import UploadFile
from pdf2image import convert_from_bytes

from src.core import get_settings


class CRUDFile:
    def __init__(
        self,
        service_name: str,
        bucket_name: str,
        aws_access_key_id: str,
        aws_secret_access_key: str,
    ) -> None:
        self.service_name = service_name
        self.bucket_name = bucket_name
        self.session = Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )

    async def upload(
        self, files: list[UploadFile], need_converted: bool = False
    ) -> list[dict[str, str]]:
        result: list[dict[str, str]] = []
        converted_files: list[UploadFile] = []

        if need_converted:
            for file_object in files:
                if file_object.content_type.split("/")[1] == "pdf":
                    byte_object = file_object.file.read()
                    images = convert_from_bytes(pdf_file=byte_object)

                    for idx, image in enumerate(images):
                        temp_file = TemporaryFile()
                        image.save(fp=temp_file, format="jpeg")
                        temp_file.seek(0)
                        converted_files.append(
                            UploadFile(
                                filename=f"{idx} {file_object.filename}",
                                file=temp_file,
                                content_type="image/jpeg",
                            )
                        )

                else:
                    converted_files.append(file_object)

        else:
            converted_files = files.copy()

        for file_object in converted_files:
            file_path = re.sub(
                pattern=r"[\s+\!\*\'\(\)\;\:\@\&\=\+\$\,\/\?\%\#\[\]]",
                repl="_",
                string=file_object.filename,
            )
            _, media_type = file_object.content_type.split("/")
            if media_type in ["jpeg", "png"]:
                file_type = "image"

            elif media_type == "pdf":
                file_type = "pdf"

            else:
                filename = file_object.filename
                raise ValueError(
                    f"Type of {filename} must be jpg/jpeg/png or pdf"
                )

            async with self.session.resource(self.service_name) as service:
                bucket = await service.Bucket(self.bucket_name)
                object_key = secrets.token_hex(24)

                objects = [
                    object
                    async for object in bucket.objects.filter(
                        Prefix=object_key
                    )
                ]
                if len(objects) > 0 and (objects[0].key == object_key):
                    object_key = secrets.token_hex(24)

                await bucket.upload_fileobj(
                    Fileobj=file_object.file,
                    Key=object_key,
                    ExtraArgs={
                        "ContentType": file_object.content_type,
                        "Tagging": parse.urlencode({"Name": file_path}),
                    },
                )

                file_url = (
                    f"https://{self.bucket_name}.s3.amazonaws.com/{object_key}"
                )
                result.append(
                    {
                        "name": file_path,
                        "url": file_url,
                        "type": file_type,
                        "key": object_key,
                    }
                )

        return result

    async def download(self, object_key: str) -> bytes | None:
        async with self.session.resource(self.service_name) as service:
            object = await service.Object(
                bucket_name=self.bucket_name, key=object_key
            )
            response = await object.get()
            file = await response["Body"].read()

            return file

    async def delete(self, object_key: str) -> dict:
        async with self.session.resource(self.service_name) as service:
            object = await service.Object(
                bucket_name=self.bucket_name, key=object_key
            )
            response = await object.delete()
            return response


file_crud = CRUDFile(
    service_name="s3",
    bucket_name=get_settings().AWS_S3_BUCKET_NAME,
    aws_access_key_id=get_settings().AWS_ACCESS_KEY_ID,
    aws_secret_access_key=get_settings().AWS_SECRET_ACCESS_KEY,
)
