from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..models import database, schemas
from ..services.ai_functions import generate_summary, enhance_note_for_notion, generate_title_and_category


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
    return enhanced_content

async def generate_summary_by_id(
        note_id: int,
        db: Session):
    note = db.query(database.Note).filter(database.Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail=f"Note with id: {note_id} not found")

    summary = None
    if note.content and len(note.content) > 100:
        try:
            summary = await generate_summary(note.content)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"AI summary generation failed: {str(e)}")

    if summary:
        note.summary = summary
        db.commit()
        db.refresh(note)
    return note

async def create(
        request: schemas.NoteCreate,
        db: Session):
    title = None
    category = None
    if request.content and len(request.content) > 100:
        try:
            title, category = await generate_title_and_category(request.content)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"AI generation failed: {str(e)}")
    new_note = database.Note(
        title=title,
        content=request.content,
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
