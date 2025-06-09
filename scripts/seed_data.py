"""
Скрипт для створення тестових даних з використанням Faker
"""
import sys
import os
from datetime import date, timedelta
from faker import Faker
from sqlalchemy.orm import Session

# Додаємо app директорію до Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.database import SessionLocal, engine, Base
from app.models import Contact

# Створюємо таблиці якщо вони не існують
Base.metadata.create_all(bind=engine)

def create_test_contacts(count: int = 20):
    """
    Створити тестові контакти з використанням Faker
    """
    fake = Faker('uk_UA')  # Український локаль
    db = SessionLocal()
    
    try:
        # Очищуємо існуючі контакти
        db.query(Contact).delete()
        db.commit()
        
        contacts = []
        for i in range(count):
            # Генеруємо дату народження (від 18 до 80 років)
            birthday = fake.date_of_birth(minimum_age=18, maximum_age=80)
            
            # Деякі контакти матимуть дні народження на найближчі 7 днів
            if i < 3:  # Перші 3 контакти
                today = date.today()
                birthday = today + timedelta(days=fake.random_int(min=1, max=7))
                birthday = birthday.replace(year=birthday.year - fake.random_int(min=20, max=50))
            
            contact = Contact(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.unique.email(),
                phone=fake.phone_number(),
                birthday=birthday,
                additional_info=fake.text(max_nb_chars=200) if fake.boolean(chance_of_getting_true=60) else None
            )
            contacts.append(contact)
        
        # Додаємо всі контакти в базу
        db.add_all(contacts)
        db.commit()
        
        print(f"✅ Створено {count} тестових контактів")
        
        # Виводимо статистику
        total_contacts = db.query(Contact).count()
        print(f"📊 Загальна кількість контактів в базі: {total_contacts}")
        
    except Exception as e:
        print(f"❌ Помилка при створенні тестових даних: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_contacts()