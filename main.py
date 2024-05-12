from fastapi import FastAPI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()


@app.get("/")
async def root():
    secret_id = os.getenv("COS_SECRET_ID", "未设置")
    secret_key = os.getenv("COS_SECRET_KEY", "未设置")
    return {"message": "Hello World","COS_SECRET_ID": secret_id, "COS_SECRET_KEY": secret_key}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
