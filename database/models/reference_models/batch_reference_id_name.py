from pydantic import BaseModel as PydanticBaseModel, Field
from typing import Optional
from bson import ObjectId

class FacultyReferenceIdName(PydanticBaseModel):
    id: ObjectId = Field(..., alias="_id", description="Batch ID")
    name: Optional[str] = Field(..., description="Batch name")
    code: str = Field(default="", description="Batch code")

    model_config = {
        "arbitrary_types_allowed": True,
        "populate_by_name": True
    }