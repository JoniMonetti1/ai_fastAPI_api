from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..models import database, schemas
from ..services.ai_functions import generate_summary_and_category, enhance_note_for_notion


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

async def enhance_by_id(
        note_id: int,
        db: Session):
    note = db.query(database.Note).filter(database.Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail=f"Note with id: {note_id} not found")

    enhanced_content = None
    if note.content and len(note.content) > 100:
        try:
            enhanced_content = await enhance_note_for_notion(note.content)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"AI enhancement failed: {str(e)}")

    if enhanced_content:
        note.content = enhanced_content
        db.commit()
        db.refresh(note)
    return note

async def create(
        request: schemas.NoteCreate,
        db: Session):
    summary = None
    category = None
    if request.content and len(request.content) > 100:
        try:
            summary, category = await generate_summary_and_category(request.content)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"AI generation failed: {str(e)}")
    new_note = database.Note(
        title=request.title,
        content=request.content,
        summary=summary,
        category=category,
        user_id=request.user_id,
    )
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
