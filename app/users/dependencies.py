from fastapi import HTTPException, status
from passlib.context import CryptContext

from app.users.dao import UsersDAO
from app.users.schemas import SUserLogin

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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
