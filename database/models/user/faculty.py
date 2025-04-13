from .base_user import User
from beanie import Indexed
from pydantic import Field
from typing import Annotated, Optional
from ..reference_models import RoomReferenceIdCode

class Faculty(User):
    code: Annotated[str, Indexed(name = "code_sparse", unique = True, sparse = True)]
    default_room: Optional[RoomReferenceIdCode] = Field(None, description="Default room for the faculty member")