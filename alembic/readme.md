# Alembic Migrations

Цей каталог містить міграції бази даних для проекту Contacts API.

## Основні команди Alembic

### Створення нової міграції
```bash
# Автоматичне створення міграції на основі змін в моделях
alembic revision --autogenerate -m "Опис змін"

# Створення порожньої міграції
alembic revision -m "Опис змін"
```

### Застосування міграцій
```bash
# Застосувати всі міграції
alembic upgrade head

# Застосувати конкретну міграцію
alembic upgrade <revision_id>

# Застосувати наступну міграцію
alembic upgrade +1
```

### Відкат міграцій
```bash
# Відкотити до попередньої версії
alembic downgrade -1

# Відкотити до конкретної версії
alembic downgrade <revision_id>

# Відкотити всі міграції
alembic downgrade base
```

### Перегляд історії
```bash
# Поточна версія
alembic current

# Історія міграцій
alembic history

# Детальна історія
alembic history --verbose
```

## Файли в цій директорії

- **env.py** - налаштування середовища Alembic
- **script.py.mako** - шаблон для нових міграцій
- **versions/** - каталог з файлами міграцій
- **README** - цей файл з документацією

## Приклад роботи з міграціями

1. Змінюємо модель в `app/models.py`
2. Створюємо міграцію: `alembic revision --autogenerate -m "Add new field"`
3. Перевіряємо згенерований файл в `versions/`
4. Застосовуємо міграцію: `alembic upgrade head`

## Налаштування

Конфігурація знаходиться в `alembic.ini` в корені проекту.
URL бази даних береться зі змінної середовища `DATABASE_URL`.