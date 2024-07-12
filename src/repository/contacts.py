from sqlalchemy.orm import Session
from typing import List, Optional
from src.schemas import ContactCreate, ContactUpdate
from src.database import models
from datetime import datetime, timedelta

def create_contact(db: Session, contact: ContactCreate):
    db_contact = models.Contact(**contact.model_dump())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def get_contacts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Contact).offset(skip).limit(limit).all()

def get_contact(db: Session, contact_id: int):
    return db.query(models.Contact).filter(models.Contact.id == contact_id).first()

def update_contact(db: Session, contact_id: int, contact: ContactUpdate):
    db_contact = get_contact(db, contact_id)
    if db_contact:
        for key, value in contact.model_dump().items():
            setattr(db_contact, key, value)
        db.commit()
        db.refresh(db_contact)
    return db_contact

def delete_contact(db: Session, contact_id: int):
    db_contact = get_contact(db, contact_id)
    if db_contact:
        db.delete(db_contact)
        db.commit()
    return db_contact

def search_contacts(db: Session, query: Optional[str] = None):
    return db.query(models.Contact).filter(
        (models.Contact.first_name.contains(query)) |
        (models.Contact.last_name.contains(query)) |
        (models.Contact.email.contains(query))
    ).all()

def get_upcoming_birthdays(db: Session, days: int = 7):
    today = datetime.today().date()
    upcoming = today + timedelta(days=days)
    current_year = today.year
    upcoming_birthdays = []

    contacts = db.query(models.Contact).all()
    for contact in contacts:
        latest_birthday = contact.birthday.replace(year=current_year)
        if today <= latest_birthday <= upcoming:
            upcoming_birthdays.append(contact)
    
    return upcoming_birthdays

