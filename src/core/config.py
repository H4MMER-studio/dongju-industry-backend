from functools import lru_cache
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    LEVEL: str
    PROJECT_TITLE: str = "동주산업 API 문서"
    PROJECT_VERSION: int = 1
    PROJECT_DESCRIPTION: str = "동주산업 API 문서"
    
    class Config:
        env_file = ".env"
        
class DevelopSettings(Settings):
    DB_URL: str =  Field(env="DEVELOP_DB_URL")
    DB_NAME: str = Field(env="DEVELOP_DB_NAME")


class ProductSettings(Settings):
    DB_URL: str = Field(env="PRODUCT_DB_URL")
    DB_NMAE: str = Field(env="PRODUCT_DB_NAME")
        
        
@lru_cache()
def get_settings():
    if Settings().LEVEL == "DEVELOP":
        return DevelopSettings()
    else:
        return ProductSettings()