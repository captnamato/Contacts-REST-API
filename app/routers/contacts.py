"""
API роутер для управління контактами (оновлений з аутентифікацією)
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from .. import crud, models, schemas
from ..database import get_db
from ..auth import get_current_verified_user

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.post("/", response_model=schemas.Contact, status_code=201)
def create_contact(
    contact: schemas.ContactCreate,
    current_user: models.User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """Створити новий контакт"""
    existing_contacts = crud.get_user_contacts(db, current_user.id, search=contact.email)
    if any(c.email == contact.email for c in existing_contacts):
        raise HTTPException(status_code=400, detail="Контакт з таким email вже існує")
    return crud.create_user_contact(db=db, contact=contact, user_id=current_user.id)


@router.get("/", response_model=List[schemas.Contact])
def read_contacts(
    skip: int = Query(0, ge=0, description="Кількість записів для пропуску"),
    limit: int = Query(100, ge=1, le=1000, description="Максимальна кількість записів"),
    search: Optional[str] = Query(None, description="Пошук за ім'ям, прізвищем або email"),
    current_user: models.User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """Отримати список контактів користувача"""
    contacts = crud.get_user_contacts(db, current_user.id, skip=skip, limit=limit, search=search)
    return contacts


@router.get("/birthdays", response_model=List[schemas.Contact])
def get_upcoming_birthdays(current_user: models.User = Depends(get_current_verified_user), db: Session = Depends(get_db)):
    """Отримати контакти з днями народження на найближчі 7 днів"""
    return crud.get_user_upcoming_birthdays(db, current_user.id)


@router.get("/{contact_id}", response_model=schemas.Contact)
def read_contact(contact_id: int, current_user: models.User = Depends(get_current_verified_user), db: Session = Depends(get_db)):
    """Отримати контакт за ID"""
    db_contact = crud.get_user_contact(db, current_user.id, contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Контакт не знайдено")
    return db_contact


@router.put("/{contact_id}", response_model=schemas.Contact)
def update_contact(
    contact_id: int,
    contact_update: schemas.ContactUpdate,
    current_user: models.User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """Оновити існуючий контакт"""
    db_contact = crud.get_user_contact(db, current_user.id, contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Контакт не знайдено")
    if contact_update.email and contact_update.email != db_contact.email:
        existing_contacts = crud.get_user_contacts(db, current_user.id, search=contact_update.email)
        if any(c.email == contact_update.email and c.id != contact_id for c in existing_contacts):
            raise HTTPException(status_code=400, detail="Контакт з таким email вже існує")
    update_data = contact_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_contact, field, value)
    db.commit()
    db.refresh(db_contact)
    return db_contact


@router.delete("/{contact_id}", status_code=204)
def delete_contact(contact_id: int, current_user: models.User = Depends(get_current_verified_user), db: Session = Depends(get_db)):
    """Видалити контакт"""
    db_contact = crud.get_user_contact(db, current_user.id, contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Контакт не знайдено")
    db.delete(db_contact)
    db.commit()
