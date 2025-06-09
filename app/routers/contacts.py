"""
API роутер для управління контактами
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from .. import crud, models, schemas
from ..database import get_db

router = APIRouter(prefix="/contacts", tags=["contacts"])

@router.post("/", response_model=schemas.Contact, status_code=201)
def create_contact(
    contact: schemas.ContactCreate, 
    db: Session = Depends(get_db)
):
    """
    Створити новий контакт
    """
    # Перевіряємо, чи не існує вже контакт з таким email
    existing_contact = crud.get_contact_by_email(db, email=contact.email)
    if existing_contact:
        raise HTTPException(status_code=400, detail="Контакт з таким email вже існує")
    
    return crud.create_contact(db=db, contact=contact)

@router.get("/", response_model=List[schemas.Contact])
def read_contacts(
    skip: int = Query(0, ge=0, description="Кількість записів для пропуску"),
    limit: int = Query(100, ge=1, le=1000, description="Максимальна кількість записів"),
    search: Optional[str] = Query(None, description="Пошук за ім'ям, прізвищем або email"),
    db: Session = Depends(get_db)
):
    """
    Отримати список контактів з можливістю пошуку
    """
    contacts = crud.get_contacts(db, skip=skip, limit=limit, search=search)
    return contacts

@router.get("/birthdays", response_model=List[schemas.Contact])
def get_upcoming_birthdays(db: Session = Depends(get_db)):
    """
    Отримати контакти з днями народження на найближчі 7 днів
    """
    return crud.get_upcoming_birthdays(db)

@router.get("/{contact_id}", response_model=schemas.Contact)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    """
    Отримати контакт за ID
    """
    db_contact = crud.get_contact(db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Контакт не знайдено")
    return db_contact

@router.put("/{contact_id}", response_model=schemas.Contact)
def update_contact(
    contact_id: int,
    contact_update: schemas.ContactUpdate,
    db: Session = Depends(get_db)
):
    """
    Оновити існуючий контакт
    """
    # Якщо оновлюється email, перевіряємо унікальність
    if contact_update.email:
        existing_contact = crud.get_contact_by_email(db, email=contact_update.email)
        if existing_contact and existing_contact.id != contact_id:
            raise HTTPException(status_code=400, detail="Контакт з таким email вже існує")
    
    db_contact = crud.update_contact(db, contact_id, contact_update)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Контакт не знайдено")
    return db_contact

@router.delete("/{contact_id}", status_code=204)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    """
    Видалити контакт
    """
    success = crud.delete_contact(db, contact_id)
    if not success:
        raise HTTPException(status_code=404, detail="Контакт не знайдено")