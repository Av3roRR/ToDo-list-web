from fastapi import APIRouter, HTTPException, status

from app.users.dao import UsersDAO
from app.users.dependencies import get_password_hash
from app.users.schemas import SUserRegistration, SUserLogin

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/register")
async def user_registration(
    user_data: SUserRegistration 
):
    user_or_none = await UsersDAO.find_one_or_none(email=user_data.email)
    if user_or_none:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Пользователь с такой почтой уже существует")
    
    user_dict = user_data.model_dump()
    user_dict['password'] = get_password_hash(user_data.password)
    
    await UsersDAO.add(**user_dict)
    
    return {"message": "Вы успешно зарегистрировались!"}


@router.post("/login")
async def user_login(
    user_data: SUserLogin
):
    user = await UsersDAO.find_one_or_none(email=user_data.email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Пользователя с такой почтой ещё не существует")
        
    