from functools import lru_cache

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    LEVEL: str
    DB_NAME: str
    PROJECT_TITLE: str = "동주산업 API 문서"
    PROJECT_VERSION: int = 1
    PROJECT_DESCRIPTION: str = "동주산업 API 문서"

    class Config:
        env_file = ".env"


class DevelopSettings(Settings):
    DB_URL: str = Field(env="DEVELOP_DB_URL")
    AWS_S3_BUCKET_NAME: str = Field(env="DEVELOP_AWS_S3_BUCKET_NAME")
    AWS_ACCESS_KEY_ID: str = Field(env="DEVELOP_AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: str = Field(env="DEVELOP_AWS_SECRET_ACCESS_KEY")


class ProductSettings(Settings):
    DB_URL: str = Field(env="PRODUCT_DB_URL")
    AWS_S3_BUCKET_NAME: str = Field(env="PRODUCT_AWS_S3_BUCKET_NAME")
    AWS_ACCESS_KEY_ID: str = Field(env="PRODUCT_AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: str = Field(env="PRODUCT_AWS_SECRET_ACCESS_KEY")


@lru_cache()
def get_settings():
    if Settings().LEVEL == "DEVELOP":
        return DevelopSettings()
    else:
        return ProductSettings()
