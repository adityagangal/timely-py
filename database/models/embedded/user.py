from pydantic import BaseModel, Field
from typing import Optional, List
from beanie import PydanticObjectId

class UserIdName(BaseModel):
    id: PydanticObjectId = Field(..., description="Id of User", alias="_id")
    name: str = Field(..., description="Name of User")

class UserIdNameTags(BaseModel):
    id: PydanticObjectId = Field(..., alias="_id", description="User document _id")
    name: str = Field(..., description="Name")
    tags: Optional[List[str]] = Field(default=[], description="Tags such as faculty, admin, etc.")

class FacultyIdNameCode(BaseModel):
    id: PydanticObjectId = Field(..., alias="_id", description="User document _id")
    name: str = Field(..., description="Faculty name")
    code: Optional[str] = Field(default="", description="Faculty Code")