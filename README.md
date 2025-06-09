# 📱 Contacts REST API

REST API для управління контактами, побудований з використанням FastAPI, SQLAlchemy та PostgreSQL.

## 🚀 Особливості

- ✅ **CRUD операції** - повний набір операцій для управління контактами
- 🔍 **Пошук контактів** - за ім'ям, прізвищем або email
- 🎂 **Дні народження** - отримання контактів з ДН на найближчі 7 днів
- ✨ **Валідація даних** - використання Pydantic для перевірки вхідних даних
- 📚 **Автодокументація** - Swagger UI та ReDoc
- 🐳 **Docker підтримка** - повна контейнеризація з Docker Compose
- 🎭 **Тестові дані** - генерація реалістичних даних з Faker

## 🛠 Технологічний стек

- **FastAPI** - сучасний веб-фреймворк для Python
- **SQLAlchemy** - ORM для роботи з базою даних
- **PostgreSQL** - реляційна база даних
- **Pydantic** - валідація та серіалізація даних
- **Poetry** - управління залежностями
- **Docker** - контейнеризація
- **Faker** - генерація тестових даних

## 📁 Структура проекту

```
contacts-api/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Основний файл додатку
│   ├── database.py             # Налаштування БД
│   ├── models.py               # SQLAlchemy моделі
│   ├── schemas.py              # Pydantic схеми
│   ├── crud.py                 # CRUD операції
│   └── routers/
│       ├── __init__.py
│       └── contacts.py         # API endpoints
├── scripts/
│   └── seed_data.py           # Тестові дані
├── .env.example               # Приклад змінних середовища
├── pyproject.toml             # Poetry конфігурація
├── Dockerfile                 # Docker конфігурація
├── docker-compose.yml         # Docker Compose
├── .gitignore                 # Git ignore
└── README.md                  # Документація
```

## ⚡ Швидкий старт

### Метод 1: Docker (рекомендовано)

```bash
# 1. Клонувати репозиторій
git clone <repository-url>
cd contacts-api

# 2. Скопіювати змінні середовища
cp .env.example .env

# 3. Запустити всі сервіси
docker-compose up -d

# 4. Створити тестові дані
docker-compose exec web python scripts/seed_data.py

# 5. Відкрити API документацію
# http://localhost:8000/docs
```

### Метод 2: Локальний розвиток

```bash
# 1. Встановити Poetry
curl -sSL https://install.python-poetry.org | python3 -

# 2. Встановити залежності
poetry install

# 3. Скопіювати та налаштувати .env
cp .env.example .env

# 4. Запустити PostgreSQL
docker run --name postgres -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres:15

# 5. Активувати віртуальне середовище
poetry shell

# 6. Створити тестові дані
python scripts/seed_data.py

# 7. Запустити додаток
uvicorn app.main:app --reload
```

## 📖 API Документація

Після запуску додатку документація буде доступна за адресами:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Основний endpoint**: http://localhost:8000/api/v1/contacts/

## 🔗 API Endpoints

### Контакти

| Метод | Endpoint | Опис |
|-------|----------|------|
| `POST` | `/api/v1/contacts/` | Створити новий контакт |
| `GET` | `/api/v1/contacts/` | Отримати список контактів |
| `GET` | `/api/v1/contacts/{id}` | Отримати контакт за ID |
| `PUT` | `/api/v1/contacts/{id}` | Оновити контакт |
| `DELETE` | `/api/v1/contacts/{id}` | Видалити контакт |
| `GET` | `/api/v1/contacts/birthdays` | Дні народження (7 днів) |

### Query параметри для пошуку

- `search` - пошук за ім'ям, прізвищем або email
- `skip` - кількість записів для пропуску (пагінація)
- `limit` - максимальна кількість записів (макс. 1000)

## 💡 Приклади використання

### Створення контакту

```bash
curl -X POST "http://localhost:8000/api/v1/contacts/" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Іван",
    "last_name": "Петренко",
    "email": "ivan.petrenko@example.com",
    "phone": "+380501234567",
    "birthday": "1990-05-15",
    "additional_info": "Друг з університету"
  }'
```

### Отримання всіх контактів

```bash
curl "http://localhost:8000/api/v1/contacts/"
```

### Пошук контактів

```bash
# Пошук за ім'ям
curl "http://localhost:8000/api/v1/contacts/?search=Іван"

# Пагінація
curl "http://localhost:8000/api/v1/contacts/?skip=10&limit=5"
```

### Дні народження

```bash
curl "http://localhost:8000/api/v1/contacts/birthdays"
```

### Оновлення контакту

```bash
curl -X PUT "http://localhost:8000/api/v1/contacts/1" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "+380507654321",
    "additional_info": "Оновлена інформація"
  }'
```

### Видалення контакту

```bash
curl -X DELETE "http://localhost:8000/api/v1/contacts/1"
```

## 🗃 Структура даних

### Модель контакту

```json
{
  "id": 1,
  "first_name": "Іван",
  "last_name": "Петренко",
  "email": "ivan.petrenko@example.com",
  "phone": "+380501234567",
  "birthday": "1990-05-15",
  "additional_info": "Додаткова інформація"
}
```

### Валідація полів

- `first_name`: 1-50 символів, обов'язкове
- `last_name`: 1-50 символів, обов'язкове
- `email`: валідний email, унікальний, обов'язковий
- `phone`: 10-20 символів, обов'язковий
- `birthday`: дата у форматі YYYY-MM-DD, обов'язкова
- `additional_info`: до 500 символів, опціональне

## 🔧 Налаштування

### Змінні середовища (.env)

```env
# База даних
DATABASE_URL=postgresql://postgres:password@localhost:5432/contacts_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=contacts_db

# Додаток
DEBUG=True
HOST=0.0.0.0
PORT=8000
```

## 🐳 Docker сервіси

- **web** - FastAPI додаток (порт 8000)
- **db** - PostgreSQL база даних (порт 5432)
- **adminer** - веб-інтерфейс для управління БД (порт 8080)

### Корисні Docker команди

```bash
# Переглянути логи
docker-compose logs -f web

# Перезапустити сервіс
docker-compose restart web

# Зупинити всі сервіси
docker-compose down

# Видалити дані БД
docker-compose down -v
```

## 🧪 Тестування

```bash
# Встановити залежності для розробки
poetry install --with dev

# Запустити тести
pytest

# Тести з покриттям
pytest --cov=app
```

## 📝 Логування та моніторинг

Додаток підтримує стандартне логування Python. Логи включають:

- HTTP запити та відповіді
- Помилки бази даних
- Валідаційні помилки
- Системні події

## 🚀 Розгортання в продакшені

### Рекомендації для продакшену:

1. **Безпека**:
   - Використовуйте HTTPS
   - Налаштуйте CORS відповідно до ваших потреб
   - Використовуйте сильні паролі для БД

2. **База даних**:
   - Використовуйте connection pooling
   - Налаштуйте backup'и
   - Моніторинг продуктивності

3. **Масштабування**:
   - Використовуйте reverse proxy (nginx)
   - Налаштуйте load balancing
   - Моніторинг ресурсів

### Docker Compose для продакшену

```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  web:
    build: .
    environment:
      - DEBUG=False
    restart: unless-stopped
  
  db:
    image: postgres:15
    restart: unless-stopped
    volumes:
      - postgres_data:/var/lib/postgresql/data
```

## 🤝 Внесок у проект

1. Форкніть репозиторій
2. Створіть нову гілку (`git checkout -b feature/amazing-feature`)
3. Зробіть коміт (`git commit -m 'Add amazing feature'`)
4. Зпушьте гілку (`git push origin feature/amazing-feature`)
5. Відкрийте Pull Request

## 📄 Ліцензія

Цей проект поширюється під ліцензією MIT. Детальніше в файлі `LICENSE`.

## 🆘 Підтримка

Якщо у вас виникли питання або проблеми:

1. Перевірте [Issues](../../issues) на GitHub
2. Створіть новий Issue з детальним описом проблеми
3. Надайте інформацію про версію Python, ОС та налаштування

## 📊 Статус проекту

- ✅ Базові CRUD операції
- ✅ Пошук та фільтрація
- ✅ Валідація даних
- ✅ Docker підтримка
- ✅ API документація
- ⏳ Автентифікація (планується)
- ⏳ Rate limiting (планується)
- ⏳ Тести покриття >90% (в розробці)