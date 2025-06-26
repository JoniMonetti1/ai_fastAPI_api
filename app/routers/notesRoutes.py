from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..auth.OAuth2 import get_current_user
from ..database import connection
from ..models import database
from ..models.schemas import ShowNote, NoteCreate, NoteUpdate
from ..repository import notesRepository

router = APIRouter(
    prefix="/notes",
    tags=["Notes"]
)

@router.get("/", response_model=List[ShowNote])
def get_all_notes(db: Session = Depends(connection.get_db),
                  current_user: database.User = Depends(get_current_user)):
    return notesRepository.get_all(db)

@router.get("/{note_id}", response_model=ShowNote, )
def get_note_by_id(
        note_id: int,
        db: Session = Depends(connection.get_db),
        current_user: database.User = Depends(get_current_user)):
    return notesRepository.get_by_id(note_id, db)

@router.get("/{note_id}/enhance", response_model=ShowNote)
async def enhance_note_by_id(
        note_id: int,
        db: Session = Depends(connection.get_db),
        current_user: database.User = Depends(get_current_user)):
    return await notesRepository.enhance_by_id(note_id, db)

@router.get("/{note_id}/summary", response_model=ShowNote)
async def generate_summary_by_id(
        note_id: int,
        db: Session = Depends(connection.get_db),
        current_user: database.User = Depends(get_current_user)):
    return await notesRepository.generate_summary_by_id(note_id, db)

@router.post("/", response_model=NoteCreate, status_code=201)
async def create_note(
        request: NoteCreate,
        db: Session = Depends(connection.get_db),
        current_user: database.User = Depends(get_current_user)):
    return await notesRepository.create(request, db)

@router.put("/{note_id}", response_model=NoteUpdate, status_code=202)
def update_note(
        note_id: int,
        request: NoteUpdate,
        db: Session = Depends(connection.get_db),
        current_user: database.User = Depends(get_current_user)):
    return notesRepository.update(note_id, request, db)

@router.delete("/{note_id}", status_code=204)
def delete_note(
        note_id: int,
        db: Session = Depends(connection.get_db),
        current_user: database.User = Depends(get_current_user)):
    return notesRepository.delete(note_id, db)