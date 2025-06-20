from pydantic import BaseModel
from typing import List, Optional

# ---------- USER SCHEMAS ----------
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class ShowUser(UserBase):
    class Config:
        from_attributes = True
