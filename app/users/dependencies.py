from datetime import datetime, timezone
from fastapi import Depends, HTTPException, Request, status
from passlib.context import CryptContext
from jose import jwt, JWTError

from app.users.dao import UsersDAO
from app.users.schemas import SUserLogin
from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_access_token(request: Request):
    token = request.cookies.get("user_access_token")
    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Вы не вошли в свою учетную запись")

    return token

async def get_current_user(token: str = Depends(get_access_token)):
    try:
        payload = jwt.decode(
            token,  settings.SECRET_KEY, settings.HASH_ALGO
        )
    except JWTError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Ошибка подтверждения авторизации")
        
    expire: str = payload.get("exp")
    if not expire or (int(expire) < datetime.now(timezone.utc).timestamp()):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Время жизни токена истекло")
    
    user_id = int(payload.get("sub"))
    if not user_id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Недостаточно информации")
    
    user = await UsersDAO.find_by_id(user_id)
    
    return user

async def user_auth(
    user_data: SUserLogin
):
    user = await UsersDAO.find_one_or_none(email=user_data.email)
    if user is None or verify_password(
        plain_password=user_data.password,
        hashed_password=user.password):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Пользователя с такой почтой ещё не существует")
        
    return user


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)



def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
