import os

from fastapi import FastAPI

from dotenv import load_dotenv
from routers import twitter, upload

# Load environment variables
load_dotenv()

app = FastAPI()

# 包含具体的路由器
app.include_router(twitter.router, prefix="/twitter", tags=["twitter"])
app.include_router(upload.router, prefix="/upload", tags=["upload"])


@app.get("/")
async def health_check():
    return {"message": "hello"}
