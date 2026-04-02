from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db

router = APIRouter()

@router.get("/")
def get_users(db: Session = Depends(get_db)):
    return {"message": "List of users"}

@router.post("/")
def create_user(db: Session = Depends(get_db)):
    return {"message": "User created"}
