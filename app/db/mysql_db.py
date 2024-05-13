from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from pydantic import BaseModel

database_url = os.environ.get('SQLALCHEMY_DATABASE_URL', 'mysql+pymysql://user:password@localhost/dbname')
engine = create_engine(database_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# 搜索的数据来源
class QueryUser(Base):
    __tablename__ = "t_query_user"

    q_id = Column(Integer, primary_key=True, index=True)
    q_user_id = Column(String)
    is_delete = Column(Integer)


#  orm_mode = True 允许模型在从 ORM 模型（如 SQLAlchemy 的模型）接收数据时，能够正确地解析数据
#  orm_mode rename from_attributes
class QueryUserSchema(BaseModel):
    q_id: int
    q_user_id: str
    is_delete: int

    class Config:
        # orm_mode = True
        from_attributes = True
