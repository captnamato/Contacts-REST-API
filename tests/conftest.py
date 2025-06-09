"""
Налаштування тестів для pytest
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import get_db, Base

# Створення тестової бази даних в пам'яті
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    """
    Перевизначення залежності бази даних для тестів
    """
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

@pytest.fixture
def client():
    """
    Фікстура для тестового клієнта FastAPI
    """
    # Створення таблиць для тестів
    Base.metadata.create_all(bind=engine)
    
    # Перевизначення залежності
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as c:
        yield c
    
    # Очищення після тестів
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def sample_contact():
    """
    Фікстура з прикладом даних контакту
    """
    return {
        "first_name": "Тест",
        "last_name": "Тестовий",
        "email": "test@example.com",
        "phone": "+380501234567",
        "birthday": "1990-01-01",
        "additional_info": "Тестовий контакт"
    }