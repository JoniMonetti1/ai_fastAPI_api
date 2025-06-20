from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..models import database, schemas
from ..hasing import Hash

def get_all(db: Session):
    users = db.query(database.User).all()
    return users

def get_by_id(
        user_id: int,
        db: Session):
    user = db.query(database.User).filter(database.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id: {user_id} not found")
    return user

def create(
        request: schemas.UserCreate,
        db: Session):
    new_user = database.User(
        username=request.username,
        email=request.email,
        password= Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user