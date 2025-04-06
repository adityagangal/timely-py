from __future__ import annotations
from ..base_model import BaseModel
# from ..batch.batch import Batch
from beanie import Link, Indexed
from pydantic import Field, EmailStr
from typing import List, TYPE_CHECKING, Annotated


if TYPE_CHECKING:
    from ..batch.batch import Batch  # Imported only for type hints

class User(BaseModel):
    name: str = Field(..., min_length=3, description="User's full name")
    email: Annotated[EmailStr, Indexed(unique=True)]
    password: str = Field(..., min_length=8, description="The user's password")
    in_batches: List[Link["Batch"]] = Field(default=[], description="Batches user is part of")
    
    class Settings:
        name = "Users"

from ..batch.batch import Batch

User.model_rebuild()