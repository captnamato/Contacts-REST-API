# 📁 Повна структура проекту Contacts API

```
contacts-api/
├── app/                           # Основний код додатку
│   ├── __init__.py               # Ініціалізація пакету
│   ├── main.py                   # Головний файл FastAPI
│   ├── database.py               # Налаштування SQLAlchemy
│   ├── models.py                 # Моделі бази даних
│   ├── schemas.py                # Pydantic схеми
│   ├── crud.py                   # CRUD операції
│   └── routers/                  # API роутери
│       ├── __init__.py
│       └── contacts.py           # Endpoints для контактів
├── tests/                        # Тести
│   ├── __init__.py
│   ├── conftest.py              # Налаштування pytest
│   └── test_contacts.py         # Тести API контактів
├── scripts/                      # Допоміжні скрипти
│   └── seed_data.py             # Створення тестових даних
├── alembic/                      # Міграції бази даних
│   ├── versions/                # Файли міграцій
│   ├── env.py                   # Налаштування Alembic
│   ├── script.py.mako           # Шаблон міграцій
│   └── README                   # Документація Alembic
├── .env                         # Змінні середовища (не в git)
├── .env.example                 # Приклад змінних середовища
├── .gitignore                   # Git ignore файл
├── .dockerignore                # Docker ignore файл
├── pyproject.toml               # Poetry конфігурація
├── poetry.lock                  # Lock файл Poetry
├── alembic.ini                  # Конфігурація Alembic
├── Dockerfile                   # Docker конфігурація
├── docker-compose.yml           # Docker Compose
└── README.md                    # Документація проекту
```

## 🗂 Опис директорій

### `/app` - Основний код
- **main.py** - точка входу FastAPI додатку
- **database.py** - налаштування підключення до БД
- **models.py** - SQLAlchemy моделі таблиць
- **schemas.py** - Pydantic схеми для валідації
- **crud.py** - функції для роботи з БД
- **routers/** - API endpoints організовані за модулями

### `/tests` - Тестування
- **conftest.py** - фікстури та налаштування pytest
- **test_contacts.py** - тести для API контактів
- **test_*.py** - додаткові тести (за потребою)

### `/scripts` - Утиліти
- **seed_data.py** - генерація тестових даних
- **backup.py** - резервне копіювання (опціонально)
- **migrate.py** - допоміжні міграції (опціонально)

### `/alembic` - Міграції
- **versions/** - історія змін схеми БД
- **env.py** - конфігурація середовища Alembic
- **script.py.mako** - шаблон для нових міграцій

## 📋 Створення структури

### Команди для створення директорій:

```bash
# Створення основної структури
mkdir -p contacts-api/{app/routers,tests,scripts,alembic/versions}

# Створення порожніх __init__.py файлів
touch contacts-api/app/__init__.py
touch contacts-api/app/routers/__init__.py
touch contacts-api/tests/__init__.py

# Перехід в директорію проекту
cd contacts-api

# Ініціалізація Poetry проекту
poetry init

# Створення віртуального середовища
poetry shell
```

### Послідовність створення файлів:

1. **Базові конфігураційні файли:**
   ```bash
   # Poetry та Python
   pyproject.toml
   .env.example
   .gitignore
   .dockerignore
   
   # Docker
   Dockerfile
   docker-compose.yml
   ```

2. **Основний код додатку:**
   ```bash
   app/__init__.py
   app/database.py      # Спочатку БД
   app/models.py        # Потім моделі
   app/schemas.py       # Схеми валідації
   app/crud.py          # CRUD операції
   app/routers/__init__.py
   app/routers/contacts.py  # API endpoints
   app/main.py          # Головний файл (останнім)
   ```

3. **Допоміжні скрипти:**
   ```bash
   scripts/seed_data.py
   ```

4. **Тести:**
   ```bash
   tests/__init__.py
   tests/conftest.py
   tests/test_contacts.py
   ```

5. **Міграції (опціонально):**
   ```bash
   alembic.ini
   alembic/env.py
   alembic/script.py.mako
   ```

6. **Документація:**
   ```bash
   README.md
   ```

## ⚙️ Налаштування Alembic

Якщо потрібно використовувати Alembic для міграцій:

```bash
# Ініціалізація Alembic
alembic init alembic

# Створення першої міграції
alembic revision --autogenerate -m "Create contacts table"

# Застосування міграцій
alembic upgrade head
```

## 🔧 Порядок запуску проекту

### 1. Початкове налаштування:
```bash
# Клонувати/створити проект
git clone <repo> && cd contacts-api

# Встановити залежності
poetry install

# Скопіювати змінні середовища
cp .env.example .env
```

### 2. Запуск бази даних:
```bash
# Через Docker
docker run --name postgres \
  -e POSTGRES_PASSWORD=password \
  -p 5432:5432 -d postgres:15

# Або через Docker Compose
docker-compose up -d db
```

### 3. Підготовка даних:
```bash
# Активувати віртуальне середовище
poetry shell

# Створити тестові дані
python scripts/seed_data.py
```

### 4. Запуск додатку:
```bash
# Режим розробки
uvicorn app.main:app --reload

# Або через Docker Compose
docker-compose up -d web
```

### 5. Перевірка роботи:
```bash
# Тест API
curl http://localhost:8000/health

# Відкрити документацію
open http://localhost:8000/docs
```

## 📝 Контрольний список створення

- [ ] Створити структуру директорій
- [ ] Налаштувати Poetry (`pyproject.toml`)
- [ ] Створити файли середовища (`.env.example`)
- [ ] Написати основний код (`app/`)
- [ ] Налаштувати Docker (`Dockerfile`, `docker-compose.yml`)
- [ ] Створити тестові дані (`scripts/seed_data.py`)
- [ ] Написати тести (`tests/`)
- [ ] Налаштувати Git (`.gitignore`)
- [ ] Написати документацію (`README.md`)
- [ ] Протестувати локальний запуск
- [ ] Протестувати Docker запуск

## 🎯 Фінальна перевірка

Після створення всіх файлів, проект повинен:

1. ✅ Запускатися локально через Poetry
2. ✅ Запускатися через Docker Compose
3. ✅ Мати робочу документацію API
4. ✅ Проходити всі тести
5. ✅ Генерувати тестові дані
6. ✅ Підтримувати всі CRUD операції
7. ✅ Мати функцію пошуку
8. ✅ Показувати найближчі дні народження

Структура готова для розробки та розгортання! 🚀