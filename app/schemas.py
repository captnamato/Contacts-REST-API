"""
Pydantic схеми для валідації даних
"""
from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field


# User схеми
class UserBase(BaseModel):
    """Базова схема користувача"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)


class UserCreate(UserBase):
    """Схема для реєстрації користувача"""
    password: str = Field(..., min_length=6, max_length=128)


class UserUpdate(BaseModel):
    """Схема для оновлення користувача"""
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    avatar_url: Optional[str] = None


class UserResponse(UserBase):
    """Схема відповіді користувача"""
    id: int
    avatar_url: Optional[str] = None
    is_active: bool
    is_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """Схема для логіну"""
    email: EmailStr
    password: str


class Token(BaseModel):
    """Схема токена"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Дані токена"""
    email: Optional[str] = None


# Contact схеми з owner_id
class ContactBase(BaseModel):
    """Базова схема контакту"""
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=20)
    birthday: date
    additional_info: Optional[str] = Field(None, max_length=500)


class ContactCreate(ContactBase):
    """Схема для створення контакту"""
    pass


class ContactUpdate(BaseModel):
    """Схема для оновлення контакту"""
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, min_length=10, max_length=20)
    birthday: Optional[date] = None
    additional_info: Optional[str] = Field(None, max_length=500)


class Contact(ContactBase):
    """Схема контакту з ідентифікатором"""
    id: int
    owner_id: int

    class Config:
        from_attributes = True


class EmailVerificationRequest(BaseModel):
    """Запит на верифікацію email"""
    email: EmailStr


class EmailVerificationResponse(BaseModel):
    """Відповідь на верифікацію email"""
    message: str
