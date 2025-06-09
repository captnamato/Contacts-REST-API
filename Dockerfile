# Використовуємо офіційний Python image
FROM python:3.11-slim

# Встановлюємо робочу директорію
WORKDIR /app

# Встановлюємо системні залежності
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Встановлюємо Poetry
RUN pip install poetry

# Копіюємо файли конфігурації Poetry
COPY pyproject.toml poetry.lock* ./

# Налаштовуємо Poetry (не створювати віртуальне середовище)
RUN poetry config virtualenvs.create false

# Встановлюємо залежності
RUN poetry install --no-dev

# Копіюємо код додатку
COPY . .

# Відкриваємо порт
EXPOSE 8000

# Команда запуску
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]