from pydantic import BaseModel, Field
import uuid
from datetime import datetime
from typing import  List
from src.books.schemas import Book

class UserCreateModel(BaseModel):
    first_name: str = Field(max_length=30)
    last_name: str = Field(max_length=30)
    username: str = Field(max_length=40)
    email: str = Field(max_length=40)
    password: str = Field(max_length=12)
    
class UserModel(BaseModel):
    uid: uuid.UUID
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool  
    password_hash: str 
    created_at: datetime 
    updated_at: datetime 
    books: List[Book]

class UserLoginModel(BaseModel):
    username: str = Field(max_length=40)
    password: str = Field(max_length=12)