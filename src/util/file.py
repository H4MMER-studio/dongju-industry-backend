import re

from aioboto3 import Session
from fastapi import UploadFile
from passlib.context import CryptContext

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
        self.file_context = CryptContext(
            schemes=["sha256_crypt"], deprecated="auto"
        )

    async def upload(self, files: list[UploadFile]) -> list[dict[str, str]]:
        result: list[dict[str, str]] = []

        for file_object in files:
            file_path = file_object.filename.replace(" ", "_")

            if re.match(r"(image\/)", file_object.content_type):
                file_type = "image"
            else:
                file_type = "others"

            async with self.session.resource(self.service_name) as service:
                bucket = await service.Bucket(self.bucket_name)
                object_key = self.file_context.hash(secret=file_path)

                await bucket.upload_fileobj(
                    Fileobj=file_object.file,
                    Key=object_key,
                    ExtraArgs={
                        "ContentType": file_object.content_type,
                        "Tagging": f"Name={file_path}",
                    },
                )

                file_url = (
                    f"https://{self.bucket_name}.s3.amazonaws.com/{file_path}"
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

    async def download(self, file_name: str) -> bytes | None:
        object_key = self.file_context.hash(file_name)
        async with self.session.resource(self.service_name) as service:
            object = await service.Object(
                bucket_name=self.bucket_name, key=object_key
            )
            response = await object.get()
            file = await response["Body"].read()

            return file

    async def delete(self, file_name: str) -> None:
        async with self.session.client(self.service_name) as service:
            await service.objects.filter(Prefix=file_name).delete()


file_crud = CRUDFile(
    service_name="s3",
    bucket_name=get_settings().AWS_S3_BUCKET_NAME,
    aws_access_key_id=get_settings().AWS_ACCESS_KEY_ID,
    aws_secret_access_key=get_settings().AWS_SECRET_ACCESS_KEY,
)
