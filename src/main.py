import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient

from src.api import router
from src.core import get_settings

app = FastAPI(
    title=get_settings().PROJECT_TITLE,
    version=get_settings().PROJECT_VERSION,
    description=get_settings().PROJECT_DESCRIPTION,
)

app.include_router(router=router)


@app.on_event("startup")
async def connect_db():
    app.db_client = AsyncIOMotorClient(get_settings().DB_URL)
    app.db = app.db_client[get_settings().DB_NAME]


@app.on_event("shutdown")
async def close_db():
    app.db_client.close()


origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5500",
    "https://dongjuind.co.kr",
    "https://www.dongjuind.co.kr",
    "https://admin.dongjuind.co.kr",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
