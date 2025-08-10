from fastapi.security import HTTPBearer
from fastapi import Request, status, Depends
from fastapi.security import HTTPAuthorizationCredentials
from .utils import decode_access_token
from fastapi.exceptions import HTTPException
from src.db.redis import  token_in_blocklist
from .service import UserService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List, Any
from .models import User


user_service = UserService()


class TokenBearer(HTTPBearer):
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds =  await super().__call__(request)
        token = creds.credentials
        token_data = decode_access_token(token)
        if not self.token_valid(token):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide a valid token",
            )

        if await token_in_blocklist(token_data['jti']):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token has been revoked",
            )

        self.verify_token_data(token_data)
            
        return token_data

    def token_valid(self, token : str) -> bool:
        token_data = decode_access_token(token)
        return True if token_data is not None else False

    def verify_token_data(self, token_data):
        raise NotImplementedError("Please override this method in subclasses")

class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data['refresh']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide a valid access token",
            )

class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data['refresh']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide a valid refresh token",
            )


async def get_current_user(
    token_data: dict = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_session)
):
    user_name = token_data["user"]["username"]
    user = await user_service.get_user_by_username(user_name, session)
    return user



class RoleChecker:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles
        
    async def __call__(self, current_user: User = Depends(get_current_user)) -> Any:
        if current_user.role in self.allowed_roles:
            return True
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action",
        )