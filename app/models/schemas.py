from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional

# ---------- USER SCHEMAS ----------
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Username must be between 3 and 50 characters.")
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=255, description="Password must be at least 8 characters long.")

    @field_validator('password')
    def validate_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not any(character.isupper() for character in value):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not any(character.islower() for character in value):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not any(character.isdigit() for character in value):
            raise ValueError("Password must contain at least one digit.")
        return value

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8, max_length=255)

    @field_validator('password')
    def validate_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not any(character.isupper() for character in value):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not any(character.islower() for character in value):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not any(character.isdigit() for character in value):
            raise ValueError("Password must contain at least one digit.")
        return value

class ShowUser(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime]
    class Config:
        from_attributes = True

# ---------- NOTE SCHEMAS ----------
class NoteBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=256, description="Title is required")
    content: str = Field(..., min_length=1, description="Content cannot be empty")
    category: Optional[str] = Field(None, max_length=50)

class NoteCreate(NoteBase):
    user_id: int

class NoteUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=256)
    content: Optional[str] = Field(None, min_length=1)
    category: Optional[str] = Field(None, max_length=50)
    is_archived: Optional[bool] = None

class ShowNote(NoteBase):
    id: int
    user_id: int
    summary: Optional[str] = None
    is_ai_processed: bool
    is_archived: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# ---------- TOKEN SCHEMAS ----------
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 3600

class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int] = None


