"""
Головний файл FastAPI додатку
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from .database import engine, Base
from .routers import contacts

# Завантажуємо змінні середовища
load_dotenv()

# Створюємо таблиці в базі даних
Base.metadata.create_all(bind=engine)

# Створюємо FastAPI додаток
app = FastAPI(
    title="Contacts API",
    description="REST API для управління контактами",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Додаємо CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Підключаємо роутери
app.include_router(contacts.router, prefix="/api/v1")

@app.get("/")
def read_root():
    """
    Кореневий endpoint
    """
    return {"message": "Contacts API працює успішно!"}

@app.get("/health")
def health_check():
    """
    Перевірка стану додатку
    """
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "True").lower() == "true"
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=debug
    )