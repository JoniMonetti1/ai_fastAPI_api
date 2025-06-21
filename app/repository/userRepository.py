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

def update(
        user_id: int,
        request: schemas.UserUpdate,
        db: Session):
    user = db.query(database.User).filter(database.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id: {user_id} not found")

    update_data = request.model_dump(exclude_unset=True)

    if 'password' in update_data and update_data['password']:
        update_data['password'] = Hash.bcrypt(update_data['password'])

    for key, value in update_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user

def delete(
        user_id: int,
        db: Session):
    user = db.query(database.User).filter(database.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id: {user_id} not found")

    db.delete(user)
    db.commit()

def get_all_notes_by_user_id(
        user_id: int,
        db: Session):
    notes = db.query(database.Note).filter(database.Note.user_id == user_id).all()
    if not notes:
        raise HTTPException(status_code=404, detail=f"No notes found for user with id: {user_id}")
    return notes