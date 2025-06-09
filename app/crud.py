"""
CRUD операції для роботи з контактами
"""
from datetime import date, timedelta
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, extract
from . import models, schemas

def get_contact(db: Session, contact_id: int) -> Optional[models.Contact]:
    """Отримати контакт за ID"""
    return db.query(models.Contact).filter(models.Contact.id == contact_id).first()

def get_contact_by_email(db: Session, email: str) -> Optional[models.Contact]:
    """Отримати контакт за email"""
    return db.query(models.Contact).filter(models.Contact.email == email).first()

def get_contacts(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    search: Optional[str] = None
) -> List[models.Contact]:
    """
    Отримати список контактів з можливістю пошуку
    """
    query = db.query(models.Contact)
    
    # Пошук за ім'ям, прізвищем або email
    if search:
        search_filter = or_(
            models.Contact.first_name.ilike(f"%{search}%"),
            models.Contact.last_name.ilike(f"%{search}%"),
            models.Contact.email.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    
    return query.offset(skip).limit(limit).all()

def get_upcoming_birthdays(db: Session) -> List[models.Contact]:
    """
    Отримати контакти з днями народження на найближчі 7 днів
    """
    today = date.today()
    end_date = today + timedelta(days=7)
    
    # Якщо період переходить через кінець року
    if today.year != end_date.year:
        return db.query(models.Contact).filter(
            or_(
                and_(
                    extract('month', models.Contact.birthday) == today.month,
                    extract('day', models.Contact.birthday) >= today.day
                ),
                and_(
                    extract('month', models.Contact.birthday) == end_date.month,
                    extract('day', models.Contact.birthday) <= end_date.day
                )
            )
        ).all()
    else:
        # Звичайний випадок в межах одного року
        return db.query(models.Contact).filter(
            and_(
                extract('month', models.Contact.birthday) == today.month,
                extract('day', models.Contact.birthday) >= today.day,
                extract('day', models.Contact.birthday) <= end_date.day
            )
        ).all()

def create_contact(db: Session, contact: schemas.ContactCreate) -> models.Contact:
    """Створити новий контакт"""
    db_contact = models.Contact(**contact.model_dump())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def update_contact(
    db: Session, 
    contact_id: int, 
    contact_update: schemas.ContactUpdate
) -> Optional[models.Contact]:
    """Оновити існуючий контакт"""
    db_contact = get_contact(db, contact_id)
    if not db_contact:
        return None
    
    # Оновлюємо тільки передані поля
    update_data = contact_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_contact, field, value)
    
    db.commit()
    db.refresh(db_contact)
    return db_contact

def delete_contact(db: Session, contact_id: int) -> bool:
    """Видалити контакт"""
    db_contact = get_contact(db, contact_id)
    if not db_contact:
        return False
    
    db.delete(db_contact)
    db.commit()
    return True