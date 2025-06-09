"""
SQLAlchemy моделі для бази даних
"""
from sqlalchemy import Column, Integer, String, Date, Text
from sqlalchemy.sql import func
from .database import Base

class Contact(Base):
    """
    Модель контакту в базі даних
    """
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False, index=True)
    last_name = Column(String(50), nullable=False, index=True)  
    email = Column(String(100), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=False)
    birthday = Column(Date, nullable=False)
    additional_info = Column(Text, nullable=True)
    
    def __repr__(self):
        return f"<Contact(id={self.id}, email='{self.email}')>"