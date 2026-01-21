from sqlalchemy import Column, Integer, String
from sqlalchemy.orm  import declarative_base
from database import Base
from pydantic import BaseModel

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, primary_key=True, index=True)
    fullname = Column(String)
    email = Column(String, index=True)
    hashed_password = Column(String)

class UserRequest(BaseModel):
    username: str
    fullname: str
    email: str
    password: str

class UserResponse(BaseModel):
    username: str
    email: str