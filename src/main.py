import uvicorn
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorGridFSBucket

from src.api import router
from src.core import get_settings

app = FastAPI(
    title=get_settings().PROJECT_TITLE,
    version=get_settings().PROJECT_VERSION,
    description=get_settings().PROJECT_DESCRIPTION,
)

app.include_router(router=router, prefix="/api")


@app.on_event("startup")
async def connect_db():
    app.db_client = AsyncIOMotorClient(get_settings().DB_URL)
    app.db = app.db_client[get_settings().DB_NAME]
    app.fs = AsyncIOMotorGridFSBucket(app.db)


@app.on_event("shutdown")
async def close_db():
    app.db_client.close()


if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
