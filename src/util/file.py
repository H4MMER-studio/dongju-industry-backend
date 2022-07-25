import re

from aioboto3 import Session
from fastapi import UploadFile

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
                await bucket.upload_fileobj(
                    Fileobj=file_object.file,
                    Key=file_path,
                    ExtraArgs={"ContentType": file_object.content_type},
                )

                file_url = (
                    f"https://{self.bucket_name}.s3.amazonaws.com/{file_path}"
                )
                result.append(
                    {"name": file_path, "url": file_url, "type": file_type}
                )

        return result

    async def download(self, file_name: str) -> bytes | None:
        async with self.session.resource(self.service_name) as service:
            object = await service.Object(self.bucket_name, file_name)
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
