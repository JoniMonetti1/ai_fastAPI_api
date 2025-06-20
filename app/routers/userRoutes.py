from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import connection
from ..models.schemas import UserBase, ShowUser, UserCreate
from ..repository import userRepository

router = APIRouter(
    prefix="/user",
    tags=["Users"]
)

@router.get("/", response_model=List[ShowUser])
def get_all_users(db: Session = Depends(connection.get_db)):
    return userRepository.get_all(db);

@router.get("/{user_id}", response_model=ShowUser)
def get_user_by_id(
        user_id: int,
        db: Session = Depends(connection.get_db)):
    return userRepository.get_by_id(user_id, db)

@router.post("/", response_model=UserCreate, status_code=201)
def create_user(
        request: UserCreate,
        db: Session = Depends(connection.get_db)):
    return userRepository.create(request, db)