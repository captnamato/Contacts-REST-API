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
from app.auth import create_access_token

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
def test_user():
    """Фікстура з тестовим користувачем"""
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123",
        "first_name": "Test",
        "last_name": "User"
    }

@pytest.fixture
def authenticated_client(client, test_user):
    """Фікстура з аутентифікованим клієнтом"""
    client.post("/api/v1/auth/register", json=test_user)
    db = TestingSessionLocal()
    from app.models import User
    user = db.query(User).filter(User.email == test_user["email"]).first()
    user.is_verified = True
    db.commit()
    db.close()
    login_response = client.post("/api/v1/auth/login", json={"email": test_user["email"], "password": test_user["password"]})
    token = login_response.json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client
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
