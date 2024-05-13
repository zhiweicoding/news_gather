from fastapi import FastAPI

from dotenv import load_dotenv
from app.routers import upload, twitter, db

# Load environment variables
load_dotenv()

app = FastAPI()

# 包含具体的路由器
app.include_router(twitter.router, prefix="/twitter", tags=["twitter"])
app.include_router(upload.router, prefix="/upload", tags=["upload"])
app.include_router(db.router, prefix="/db", tags=["db"])


@app.get("/")
async def health_check():
    return {"message": "hello"}
