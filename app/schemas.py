"""
Pydantic схеми для валідації даних
"""
from datetime import date
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class ContactBase(BaseModel):
    """Базова схема контакту"""
    first_name: str = Field(..., min_length=1, max_length=50, description="Ім'я контакту")
    last_name: str = Field(..., min_length=1, max_length=50, description="Прізвище контакту")
    email: EmailStr = Field(..., description="Електронна адреса")
    phone: str = Field(..., min_length=10, max_length=20, description="Номер телефону")
    birthday: date = Field(..., description="День народження")
    additional_info: Optional[str] = Field(None, max_length=500, description="Додаткова інформація")

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

    class Config:
        from_attributes = True