from pydantic import BaseModel as PydanticBaseModel, Field
from bson import ObjectId

class SubjectReferenceIdName(PydanticBaseModel):
    id: ObjectId = Field(..., alias="_id", description="Subject ID")
    name: str = Field(..., description="Subject name")

    model_config = {
        "arbitrary_types_allowed": True,
        "populate_by_name": True
    }