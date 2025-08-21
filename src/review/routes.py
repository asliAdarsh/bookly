from fastapi import APIRouter, Depends
from src.db.models import User
from .schemas import ReviewCreateModel
from src.db.main import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from .services import ReviewService
from src.auth.dependencies import get_current_user

review_router = APIRouter()
review_service = ReviewService()

@review_router.post('/book/{book_uid}/review')
async def add_review_to_book(
    book_uid: str,
    review_data: ReviewCreateModel,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    new_review = await review_service.add_review_to_book(
        user_username = user.username,
        review_data= review_data,
        book_uid= book_uid,
        session= session
    )
    
    return new_review