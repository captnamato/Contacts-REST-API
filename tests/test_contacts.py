"""
Тести для API контактів
"""
import pytest
from datetime import date, timedelta
from tests.conftest import authenticated_client

def test_create_contact(authenticated_client, sample_contact):
    """Тест створення контакту"""
    response = authenticated_client.post("/api/v1/contacts/", json=sample_contact)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == sample_contact["email"]
    assert data["first_name"] == sample_contact["first_name"]
    assert "id" in data

def test_create_contact_duplicate_email(authenticated_client, sample_contact):
    """Тест створення контакту з дублікатом email"""
    # Створюємо перший контакт
    authenticated_client.post("/api/v1/contacts/", json=sample_contact)
    
    # Спробуємо створити другий з тим же email
    response = authenticated_client.post("/api/v1/contacts/", json=sample_contact)
    assert response.status_code == 400
    assert "вже існує" in response.json()["detail"]

def test_get_contacts(authenticated_client, sample_contact):
    """Тест отримання списку контактів"""
    # Створюємо контакт
    authenticated_client.post("/api/v1/contacts/", json=sample_contact)
    
    # Отримуємо список
    response = authenticated_client.get("/api/v1/contacts/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["email"] == sample_contact["email"]

def test_get_contact_by_id(authenticated_client, sample_contact):
    """Тест отримання контакту за ID"""
    # Створюємо контакт
    create_response = authenticated_client.post("/api/v1/contacts/", json=sample_contact)
    contact_id = create_response.json()["id"]
    
    # Отримуємо за ID
    response = authenticated_client.get(f"/api/v1/contacts/{contact_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == contact_id
    assert data["email"] == sample_contact["email"]

def test_get_contact_not_found(authenticated_client):
    """Тест отримання неіснуючого контакту"""
    response = authenticated_client.get("/api/v1/contacts/999")
    assert response.status_code == 404

def test_update_contact(authenticated_client, sample_contact):
    """Тест оновлення контакту"""
    # Створюємо контакт
    create_response = authenticated_client.post("/api/v1/contacts/", json=sample_contact)
    contact_id = create_response.json()["id"]
    
    # Оновлюємо
    update_data = {"first_name": "Оновлений", "phone": "+380507654321"}
    response = authenticated_client.put(f"/api/v1/contacts/{contact_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "Оновлений"
    assert data["phone"] == "+380507654321"
    assert data["email"] == sample_contact["email"]  # Не змінилось

def test_update_contact_not_found(authenticated_client):
    """Тест оновлення неіснуючого контакту"""
    update_data = {"first_name": "Тест"}
    response = authenticated_client.put("/api/v1/contacts/999", json=update_data)
    assert response.status_code == 404

def test_delete_contact(authenticated_client, sample_contact):
    """Тест видалення контакту"""
    # Створюємо контакт
    create_response = authenticated_client.post("/api/v1/contacts/", json=sample_contact)
    contact_id = create_response.json()["id"]
    
    # Видаляємо
    response = authenticated_client.delete(f"/api/v1/contacts/{contact_id}")
    assert response.status_code == 204
    
    # Перевіряємо, що видалено
    get_response = authenticated_client.get(f"/api/v1/contacts/{contact_id}")
    assert get_response.status_code == 404

def test_delete_contact_not_found(authenticated_client):
    """Тест видалення неіснуючого контакту"""
    response = authenticated_client.delete("/api/v1/contacts/999")
    assert response.status_code == 404

def test_search_contacts(authenticated_client):
    """Тест пошуку контактів"""
    # Створюємо кілька контактів
    contacts = [
        {
            "first_name": "Іван",
            "last_name": "Петренко",
            "email": "ivan@example.com",
            "phone": "+380501111111",
            "birthday": "1990-01-01"
        },
        {
            "first_name": "Марія",
            "last_name": "Іваненко",
            "email": "maria@example.com",
            "phone": "+380502222222",
            "birthday": "1992-02-02"
        }
    ]
    
    for contact in contacts:
        authenticated_client.post("/api/v1/contacts/", json=contact)
    
    # Пошук за ім'ям
    response = authenticated_client.get("/api/v1/contacts/?search=Іван")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2  # Іван і Іваненко
    
    # Пошук за email
    response = authenticated_client.get("/api/v1/contacts/?search=maria")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["first_name"] == "Марія"

def test_pagination(authenticated_client):
    """Тест пагінації"""
    # Створюємо кілька контактів
    for i in range(5):
        contact = {
            "first_name": f"Тест{i}",
            "last_name": "Тестовий",
            "email": f"test{i}@example.com",
            "phone": f"+38050123456{i}",
            "birthday": "1990-01-01"
        }
        authenticated_client.post("/api/v1/contacts/", json=contact)
    
    # Тест limit
    response = authenticated_client.get("/api/v1/contacts/?limit=3")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    
    # Тест skip
    response = authenticated_client.get("/api/v1/contacts/?skip=2&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

def test_upcoming_birthdays(authenticated_client):
    """Тест отримання днів народження"""
    today = date.today()
    tomorrow = today + timedelta(days=1)
    next_week = today + timedelta(days=8)  # Поза межами 7 днів
    
    contacts = [
        {
            "first_name": "Завтра",
            "last_name": "Тестовий",
            "email": "tomorrow@example.com",
            "phone": "+380501111111",
            "birthday": tomorrow.isoformat()
        },
        {
            "first_name": "Наступний",
            "last_name": "Тиждень",
            "email": "nextweek@example.com",
            "phone": "+380502222222",
            "birthday": next_week.isoformat()
        }
    ]
    
    for contact in contacts:
        authenticated_client.post("/api/v1/contacts/", json=contact)
    
    response = authenticated_client.get("/api/v1/contacts/birthdays")
    assert response.status_code == 200
    data = response.json()
    # Повинен бути тільки контакт з завтрашнім ДН
    assert len(data) == 1
    assert data[0]["first_name"] == "Завтра"

def test_validation_errors(authenticated_client):
    """Тест валідаційних помилок"""
    # Невалідний email
    invalid_contact = {
        "first_name": "Тест",
        "last_name": "Тестовий",
        "email": "invalid-email",
        "phone": "+380501234567",
        "birthday": "1990-01-01"
    }
    
    response = authenticated_client.post("/api/v1/contacts/", json=invalid_contact)
    assert response.status_code == 422
    
    # Пусте ім'я
    invalid_contact["email"] = "valid@example.com"
    invalid_contact["first_name"] = ""
    
    response = authenticated_client.post("/api/v1/contacts/", json=invalid_contact)
    assert response.status_code == 422

def test_health_check(client):
    """Тест health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_root_endpoint(client):
    """Тест кореневого endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "працює успішно" in response.json()["message"]

