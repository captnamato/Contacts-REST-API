"""
CRUD операції для роботи з контактами та користувачами
"""
from datetime import date, timedelta, datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, extract
from . import models, schemas
from .auth import get_password_hash, verify_password, generate_verification_token


# User CRUD операції

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """Отримати користувача за email"""
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    """Отримати користувача за username"""
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """Створити нового користувача"""
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, email: str, password: str) -> Optional[models.User]:
    """Аутентифікація користувача"""
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def update_user(db: Session, user: models.User, user_update: schemas.UserUpdate) -> models.User:
    """Оновити користувача"""
    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user


def create_verification_token(db: Session, user_id: int) -> str:
    """Створити токен верифікації"""
    token = generate_verification_token()
    expires_at = datetime.utcnow() + timedelta(hours=24)
    db_verification = models.EmailVerification(user_id=user_id, token=token, expires_at=expires_at)
    db.add(db_verification)
    db.commit()
    return token


def verify_email_token(db: Session, token: str) -> Optional[models.User]:
    """Верифікувати email токен"""
    verification = db.query(models.EmailVerification).filter(
        models.EmailVerification.token == token,
        models.EmailVerification.is_used == False,
        models.EmailVerification.expires_at > datetime.utcnow()
    ).first()
    if not verification:
        return None
    verification.is_used = True
    user = db.query(models.User).filter(models.User.id == verification.user_id).first()
    if user:
        user.is_verified = True
    db.commit()
    return user


# Оновлені Contact CRUD операції з owner_id

def get_user_contacts(db: Session, user_id: int, skip: int = 0, limit: int = 100, search: Optional[str] = None) -> List[models.Contact]:
    """Отримати контакти користувача"""
    query = db.query(models.Contact).filter(models.Contact.owner_id == user_id)
    if search:
        search_filter = or_(
            models.Contact.first_name.ilike(f"%{search}%"),
            models.Contact.last_name.ilike(f"%{search}%"),
            models.Contact.email.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    return query.offset(skip).limit(limit).all()


def get_user_contact(db: Session, user_id: int, contact_id: int) -> Optional[models.Contact]:
    """Отримати контакт користувача за ID"""
    return db.query(models.Contact).filter(models.Contact.id == contact_id, models.Contact.owner_id == user_id).first()


def create_user_contact(db: Session, contact: schemas.ContactCreate, user_id: int) -> models.Contact:
    """Створити контакт для користувача"""
    db_contact = models.Contact(**contact.model_dump(), owner_id=user_id)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def get_user_upcoming_birthdays(db: Session, user_id: int) -> List[models.Contact]:
    """Отримати найближчі дні народження користувача"""
    today = date.today()
    end_date = today + timedelta(days=7)
    query = db.query(models.Contact).filter(models.Contact.owner_id == user_id)
    if today.year != end_date.year:
        return query.filter(
            or_(
                and_(
                    extract('month', models.Contact.birthday) == today.month,
                    extract('day', models.Contact.birthday) >= today.day,
                ),
                and_(
                    extract('month', models.Contact.birthday) == end_date.month,
                    extract('day', models.Contact.birthday) <= end_date.day,
                ),
            )
        ).all()
    else:
        return query.filter(
            and_(
                extract('month', models.Contact.birthday) == today.month,
                extract('day', models.Contact.birthday) >= today.day,
                extract('day', models.Contact.birthday) <= end_date.day,
            )
        ).all()
