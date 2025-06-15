"""
Налаштування бази даних SQLAlchemy
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# URL підключення до бази даних
# За замовчуванням використовується локальна SQLite база. Для підключення до
# PostgreSQL або іншої СУБД необхідно перевизначити змінну середовища
# `DATABASE_URL` у файлі `.env`.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./contacts.db")

# Створення engine для підключення до БД
engine = create_engine(DATABASE_URL)

# Створення сесії для роботи з БД
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовий клас для всіх моделей
Base = declarative_base()

def get_db():
    """
    Залежність для отримання сесії бази даних
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()