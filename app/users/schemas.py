from pydantic import BaseModel, EmailStr, Field

class SUserRegistration(BaseModel):
    name: str = Field(min_length=3, alias="username")
    surname: str = Field(min_length=3)
    email: EmailStr = Field(min_length=10)
    password: str
    

class SUserLogin(BaseModel):
    email: EmailStr = Field(min_length=10)
    password: str