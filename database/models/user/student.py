from .base_user import User
from pydantic import Field
from beanie import Indexed
from typing import Annotated
from pymongo import ASCENDING

class Student(User):
    uid: Annotated[str, Indexed(name = "uid_sparse", unique = True, sparse = True)]
    semester: int = Field(..., description="Current semester")
    division: str = Field(..., description="Student division")
    passout: int = Field(..., description="Year of graduation")
