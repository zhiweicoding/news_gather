from fastapi import APIRouter, Request
from app.entity.base_response import BaseResponse

router = APIRouter()


@router.post("/receive/list", response_model=BaseResponse)
async def receive_list(request: Request):
    # Parse the incoming JSON data
    data = await request.json()

    # You can process the data here
    print(data)

    return BaseResponse(code=200, message="success").json()
