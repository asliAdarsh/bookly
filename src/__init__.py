from fastapi import FastAPI
from .books.routes import book_router
from contextlib import asynccontextmanager
from src.db.main import init_db
from .auth.routes import auth_router

@asynccontextmanager
async def life_span(app: FastAPI):
    print(f"Server is starting ...")
    await init_db()
    yield
    print(f"Sever has been stopped...")
    

version = "v1"

app = FastAPI(
    title="Book API",
    description="API for managing books",
    version=version,
)

app.include_router(book_router, prefix=f"/api/{version}/book", tags=["books"])
app.include_router(auth_router, prefix=f"/api/{version}/user", tags=["users"])

