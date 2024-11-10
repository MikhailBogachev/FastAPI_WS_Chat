from pydantic import BaseModel, EmailStr, Field


class UserRegisterSchema(BaseModel):
    email: EmailStr = Field(..., description='Электронная почта')
    password: str = Field(..., min_length=5, max_length=50, description='Парооль от 5 до 50 символов')
    password_check: str = Field(..., min_length=5, max_length=50, description='Парооль от 5 до 50 символов')
    name: str = Field(..., min_length=3, max_length=50, description='Имя, от 3 до 50 символов')


class UserAuthSchema(BaseModel):
    email: EmailStr = Field(..., description='Электронная почта')
    password: str = Field(..., min_length=5, max_length=50, description='Парооль от 5 до 50 символов')