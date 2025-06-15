"""
Головний файл FastAPI додатку з аутентифікацією
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from .database import engine, Base
from .routers import contacts, auth
from .rate_limiter import setup_rate_limiting

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Contacts API with Authentication",
    description="REST API для управління контактами з аутентифікацією та авторизацією",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

setup_rate_limiting(app)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(contacts.router, prefix="/api/v1")


@app.get("/")
def read_root():
    """Кореневий endpoint"""
    return {
        "message": "Contacts API з аутентифікацією працює успішно!",
        "version": "2.0.0",
        "features": [
            "JWT Authentication",
            "Email Verification",
            "Avatar Upload",
            "Rate Limiting",
            "CORS Support",
        ],
    }


@app.get("/health")
def health_check():
    """Перевірка стану додатку"""
    return {"status": "healthy", "version": "2.0.0"}


if __name__ == "__main__":
    import uvicorn

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "True").lower() == "true"

    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=debug,
    )
