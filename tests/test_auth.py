"""
Тести для аутентифікації та авторизації
"""
import pytest
from tests.conftest import TestingSessionLocal


def test_user_registration(client, test_user):
    """Тест реєстрації користувача"""
    response = client.post("/api/v1/auth/register", json=test_user)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == test_user["email"]
    assert data["username"] == test_user["username"]
    assert "id" in data
    assert not data["is_verified"]


def test_user_registration_duplicate_email(client, test_user):
    """Тест реєстрації з дублікатом email"""
    client.post("/api/v1/auth/register", json=test_user)
    response = client.post("/api/v1/auth/register", json=test_user)
    assert response.status_code == 409


def test_user_login_success(client, test_user):
    """Тест успішного логіну"""
    client.post("/api/v1/auth/register", json=test_user)
    db = TestingSessionLocal()
    from app.models import User
    user = db.query(User).filter(User.email == test_user["email"]).first()
    user.is_verified = True
    db.commit()
    db.close()
    response = client.post("/api/v1/auth/login", json={"email": test_user["email"], "password": test_user["password"]})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_user_login_invalid_credentials(client, test_user):
    """Тест логіну з невірними даними"""
    response = client.post("/api/v1/auth/login", json={"email": test_user["email"], "password": "wrongpassword"})
    assert response.status_code == 401


def test_get_current_user(authenticated_client, test_user):
    """Тест отримання інформації про поточного користувача"""
    response = authenticated_client.get("/api/v1/auth/me")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user["email"]
    assert data["username"] == test_user["username"]


def test_update_current_user(authenticated_client):
    """Тест оновлення інформації користувача"""
    update_data = {"first_name": "Updated", "last_name": "Name"}
    response = authenticated_client.put("/api/v1/auth/me", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "Updated"
    assert data["last_name"] == "Name"


def test_unauthorized_access(client):
    """Тест доступу без токена"""
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 403


def test_invalid_token(client):
    """Тест з невірним токеном"""
    client.headers.update({"Authorization": "Bearer invalid-token"})
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401

