from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import connection
from ..models.schemas import ShowUser, UserCreate, UserUpdate, ShowNote
from ..repository import userRepository

router = APIRouter(
    prefix="/user",
    tags=["Users"]
)

@router.get("/", response_model=List[ShowUser])
def get_all_users(db: Session = Depends(connection.get_db)):
    return userRepository.get_all(db)

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

@router.put("/{user_id}", response_model=UserUpdate, status_code=202)
def update_user(
        user_id: int,
        request: UserUpdate,
        db: Session = Depends(connection.get_db)):
    return userRepository.update(user_id, request, db)

@router.delete("/{user_id}", status_code=204)
def delete_user(
        user_id: int,
        db: Session = Depends(connection.get_db)):
    return userRepository.delete(user_id, db)

@router.get("/{user_id}/notes", response_model=List[ShowNote])
def get_user_notes_by_id(
        user_id: int,
        db: Session = Depends(connection.get_db)):
    return userRepository.get_all_notes_by_user_id(user_id, db)