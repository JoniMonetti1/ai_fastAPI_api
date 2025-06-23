from datetime import datetime

from pydantic import BaseModel
from typing import List, Optional

# ---------- USER SCHEMAS ----------
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

class ShowUser(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

# ---------- NOTE SCHEMAS ----------
class NoteBase(BaseModel):
    title: str
    content: str
    summary: Optional[str] = ""
    category: Optional[str] = None

class NoteCreate(NoteBase):
    user_id: int

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    summary: Optional[str] = None
    category: Optional[str] = None

class ShowNote(NoteBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


