from fastapi import APIRouter, Depends, HTTPException, status
from src.auth.schemas import UserCreateModel, UserModel, UserLoginModel
from .service import UserService
from src.db.main import get_session
from src.auth.utils import create_access_token, verify_password
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import timedelta, datetime
from fastapi.responses import JSONResponse
from .dependencies import AccessTokenBearer, RefreshTokenBearer, get_current_user, RoleChecker
from src.db.redis import add_jti_to_blocklist

auth_router = APIRouter()
role_checker = RoleChecker(["admin", "user"])  # Example roles, adjust as needed
REFRESH_TOKEN_EXPIRY_DAYS = 2


@auth_router.get('/me', response_model=UserModel)
async def get_current_user_data(user: dict = Depends(get_current_user), _:bool = Depends(role_checker)):
    return user

@auth_router.post(
    '/signup',
    response_model= UserModel,
    status_code=status.HTTP_201_CREATED
    )
async def create_user_account(user_data: UserCreateModel, session:AsyncSession = Depends(get_session)):
    service = UserService()  
    username = user_data.username

    user_exists = await service.user_exists(username, session)
    if user_exists:
        raise HTTPException(
           status_code=status.HTTP_403_FORBIDDEN,
           detail= "User with this username already exists"
        )
    new_user = await service.create_user(user_data, session) 
    
    return new_user    
    
    
@auth_router.post('/login', ) 
async def login_user(login_data: UserLoginModel, session: AsyncSession = Depends(get_session)):
    service = UserService() 
    username = login_data.username
    password = login_data.password
    
    user = await service.get_user_by_username(username, session)
    
    if user is not None :
        password_valid = verify_password(password, user.password_hash)
    
        if password_valid:
            access_token = create_access_token(
                user_data={
                    "username": user.username,
                    "user_uid": str(user.uid),
                    "role": user.role
                    }
            )

            refresh_token = create_access_token(
                user_data={
                    "username": user.username,
                    "user_uid": str(user.uid),
                    "role": user.role
                },
                refresh=True,
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY_DAYS)
            )

            return JSONResponse(
                content={
                    "message": "Login Successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user":{
                        "username": user.username,
                        "user_uid": str(user.uid)
                    }
                }
            )
            
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Invalid login credentials"
    )
        
        
@auth_router.get('/refresh-token')
async def get_new_access_token(token_data: dict = Depends(RefreshTokenBearer())):
    expiry_date = token_data['exp']

    if datetime.fromtimestamp(expiry_date) > datetime.now():
        new_access_token = create_access_token(user_data=token_data['user'])
        return JSONResponse(content={"access_token": new_access_token})
    
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Refresh token has expired, please login again"
    )
    
@auth_router.get('/logout')
async def logout_user(token_data: dict = Depends(AccessTokenBearer())):
    jti = token_data['jti']
    
    await add_jti_to_blocklist(jti)
    return JSONResponse(
        content={
            "message": "Logout successful",
            "jti": jti
        },
        status_code=status.HTTP_200_OK
    )
    
    
