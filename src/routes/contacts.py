from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from src.schemas import Contact, ContactCreate, ContactUpdate
from src.database import db
from src.repository import contacts as contact_repository

router = APIRouter()

@router.post("/", response_model=Contact)
def create_contact(contact: ContactCreate, db: Session = Depends(db.get_db)):
    return contact_repository.create_contact(db, contact)

@router.get("/", response_model=List[Contact])
def read_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(db.get_db)):
    return contact_repository.get_contacts(db, skip=skip, limit=limit)

@router.get("/{contact_id}", response_model=Contact)
def read_contact(contact_id: int, db: Session = Depends(db.get_db)):
    db_contact = contact_repository.get_contact(db, contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@router.put("/{contact_id}", response_model=Contact)
def update_contact(contact_id: int, contact: ContactUpdate, db: Session = Depends(db.get_db)):
    db_contact = contact_repository.update_contact(db, contact_id, contact)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@router.delete("/{contact_id}", response_model=Contact)
def delete_contact(contact_id: int, db: Session = Depends(db.get_db)):
    db_contact = contact_repository.delete_contact(db, contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@router.get("/search/", response_model=List[Contact])
def search_contacts(query: Optional[str] = None, db: Session = Depends(db.get_db)):
    return contact_repository.search_contacts(db, query=query)

@router.get("/birthdays/", response_model=List[Contact])
def upcoming_birthdays(db: Session = Depends(db.get_db), days: int = 7):
    return contact_repository.get_upcoming_birthdays(db, days=days)
