from fastapi import APIRouter, Request, Depends, HTTPException
from app.entity.base_response import BaseResponse
from app.db.mysql_db import QueryUser, QueryUserSchema
from app.dependencies import get_db
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/query/list", response_model=BaseResponse)
async def query_list(db: Session = Depends(get_db)):
    query_array = db.query(QueryUser).filter(QueryUser.is_delete > 0).all()
    if query_array is None:
        raise HTTPException(status_code=500, detail="data not found")
    return BaseResponse(code=200, message="success",
                        data=[QueryUserSchema.from_orm(item) for item in query_array]).json()
