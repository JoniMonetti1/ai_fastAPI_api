from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..models import database, schemas

def get_all(db: Session):
    notes = db.query(database.Note).all()
    return notes

def get_by_id(
        note_id: int,
        db: Session):
    note = db.query(database.Note).filter(database.Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail=f"Note with id: {note_id} not found")
    return note

def create(
        request: schemas.NoteCreate,
        db: Session):
    new_note = database.Note(**request.model_dump())
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

def update(
        note_id: int,
        request: schemas.NoteUpdate,
        db: Session):
    note = db.query(database.Note).filter(database.Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail=f"Note with id: {note_id} not found")

    update_data = request.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(note, key, value)

    db.commit()
    db.refresh(note)
    return note

def delete(
        note_id: int,
        db: Session):
    note = db.query(database.Note).filter(database.Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail=f"Note with id: {note_id} not found")

    db.delete(note)
    db.commit()
    return {"detail": "Note deleted successfully"}
