from __future__ import annotations
from ..base_model import BaseModel
# from ..batch.batch import Batch
from beanie import Link, Indexed
from pydantic import Field, EmailStr
from typing import List, TYPE_CHECKING, Annotated, Optional
from ..reference_models import EventReferenceEmbedded, BatchReferenceIdName


# if TYPE_CHECKING:
#     from ..batch.batch import Batch  # Imported only for type hints

class User(BaseModel):
    name: str = Field(..., min_length=3, description="User's full name")
    email: Annotated[EmailStr, Indexed(unique=True)]
    password: str = Field(..., min_length=8, description="The user's password")
    in_batches: Optional[List[BatchReferenceIdName]] = Field(default=[], description="Batches user is part of")
    faculty_events: Optional[List[EventReferenceEmbedded]] = Field(default=[], description="Events as Faculty")
    
    class Settings:
        name = "Users"

# from ..batch.batch import Batch

User.model_rebuild()