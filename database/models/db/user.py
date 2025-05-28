from __future__ import annotations
from ..core import BaseDocument
from beanie import Link, Indexed
from pydantic import Field, EmailStr
from typing import List, Annotated, Optional
from ..embedded import RecurringEventEmbedded, BatchIdNameCode, RoomIdCode
from bson import ObjectId

class User(BaseDocument):
    name: str = Field(..., min_length=3, description="User's full name")
    email: Annotated[EmailStr, Indexed(unique=True)]
    password: str = Field(..., min_length=8, description="The user's password")
    in_batches: Optional[List[BatchIdNameCode]] = Field(default=[], description="Batches user is part of")
    faculty_events: Optional[List[RecurringEventEmbedded]] = Field(default=[], description="Events as Faculty")
    
    class Settings:
        name = "Users"
    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True

class Faculty(User):
    code: Annotated[str, Indexed(name = "code_sparse", unique = True, sparse = True)]
    default_room: Optional[RoomIdCode] = Field(None, description="Default room for the faculty member")

class Student(User):
    uid: Annotated[str, Indexed(name = "uid_sparse", unique = True, sparse = True)]
    semester: int = Field(..., description="Current semester")
    division: str = Field(..., description="Student division")
    passout: int = Field(..., description="Year of graduation")
