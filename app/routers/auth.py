"""
API роутер для аутентифікації та авторизації
"""
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Request
from sqlalchemy.orm import Session
from .. import crud, models, schemas
from ..database import get_db
from ..auth import (
    create_access_token,
    get_current_user,
    get_current_verified_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from ..email import send_verification_email
from ..cloudinary_service import upload_avatar
from ..rate_limiter import limiter

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=schemas.UserResponse, status_code=201)
async def register_user(user: schemas.UserCreate, request: Request, db: Session = Depends(get_db)):
    """Реєстрація нового користувача"""
    if crud.get_user_by_email(db, email=user.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Користувач з таким email вже існує")
    if crud.get_user_by_username(db, username=user.username):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Користувач з таким username вже існує")
    db_user = crud.create_user(db, user)
    verification_token = crud.create_verification_token(db, db_user.id)
    base_url = f"{request.url.scheme}://{request.url.netloc}"
    try:
        await send_verification_email(user.email, verification_token, base_url)
    except Exception as e:
        print(f"Помилка відправки email: {e}")
    return db_user


@router.post("/login", response_model=schemas.Token)
def login_user(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    """Аутентифікація користувача"""
    user = crud.authenticate_user(db, user_credentials.email, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невірні облікові дані",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):
    """Верифікація email адреси"""
    user = crud.verify_email_token(db, token)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Невірний або застарілий токен")
    return {"message": "Email успішно верифіковано"}


@router.post("/resend-verification")
async def resend_verification(email_request: schemas.EmailVerificationRequest, request: Request, db: Session = Depends(get_db)):
    """Повторна відправка листа верифікації"""
    user = crud.get_user_by_email(db, email_request.email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Користувач не знайдений")
    if user.is_verified:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email вже верифіковано")
    verification_token = crud.create_verification_token(db, user.id)
    base_url = f"{request.url.scheme}://{request.url.netloc}"
    await send_verification_email(user.email, verification_token, base_url)
    return {"message": "Лист верифікації відправлено"}


@router.get("/me", response_model=schemas.UserResponse)
@limiter.limit("10/minute")
def get_current_user_info(request: Request, current_user: models.User = Depends(get_current_verified_user)):
    """Отримання інформації про поточного користувача"""
    return current_user


@router.put("/me", response_model=schemas.UserResponse)
def update_current_user(user_update: schemas.UserUpdate, current_user: models.User = Depends(get_current_verified_user), db: Session = Depends(get_db)):
    """Оновлення інформації поточного користувача"""
    return crud.update_user(db, current_user, user_update)


@router.post("/me/avatar", response_model=schemas.UserResponse)
async def upload_user_avatar(
    file: UploadFile = File(...),
    current_user: models.User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """Завантаження аватара користувача"""
    avatar_url = await upload_avatar(file, current_user.id)
    user_update = schemas.UserUpdate(avatar_url=avatar_url)
    updated_user = crud.update_user(db, current_user, user_update)
    return updated_user
