from pydantic import BaseModel
import uuid
from datetime import datetime,date
from typing import Optional

#Getting book data
class Book(BaseModel): # This is the schema for the Book model which will be used for serialization and validation
    uid: uuid.UUID
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    created_at: datetime
    updated_at: datetime

#Creating book data
class BookCreateModel(BaseModel): # This is the schema for creating a new book, it does not include uid, created_at, and updated_at
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    
    
# Updating book data
class BookUpdateModel(BaseModel): # This is the schema for updating an existing book, all fields are optional
    title: Optional[str] = None
    author: Optional[str] = None
    publisher: Optional[str] = None
    published_date: Optional[date] = None
    page_count: Optional[int] = None
    language: Optional[str] = None        