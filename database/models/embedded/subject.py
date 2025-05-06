from pydantic import BaseModel, Field
from beanie import PydanticObjectId

class SubjectIdName(BaseModel):
    id: PydanticObjectId = Field(..., alias="_id", description="Subject ID")
    name: str = Field(..., description="Subject name")