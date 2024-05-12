from pydantic import BaseModel


class BaseResponse(BaseModel):
    code: int
    message: str = None
    data: dict = None

    def json(self, **kwargs):
        return {"code": self.code, "message": self.message, "data": self.data}
