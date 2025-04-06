from .base_user import User
from beanie import Indexed
from pydantic import Field

class Faculty(User):
    faculty_code: str = Indexed(str, unique=True, description="Unique code for each faculty")
    default_room: str = Field(None, description="Default room for the faculty member")