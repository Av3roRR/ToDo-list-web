from fastapi import APIRouter, HTTPException, Response, status

from app.users.dao import UsersDAO
from app.users.dependencies import get_password_hash, user_auth, verify_password
from app.users.schemas import SUserRegistration, SUserLogin
from app.users.auth import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/registration")
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
async def user_authentication(
    response: Response,
    user_data: SUserLogin
):
    check = await user_auth(user_data=user_data)
    if check is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Неверная почта или пароль")
    
    access_token = create_access_token({"sub": str(check.id)})
    
    response.set_cookie(key="user_access_token", value=access_token, httponly=True)
    return {"access_token": access_token, "refresh_token": None}