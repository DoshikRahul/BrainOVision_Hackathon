from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db

router = APIRouter()

@router.get("/")
def get_reminders(db: Session = Depends(get_db)):
    return {"message": "List of reminders"}

@router.post("/")
def create_reminder(db: Session = Depends(get_db)):
    return {"message": "Reminder created"}
