from pydantic import BaseModel as PydanticBaseModel, Field
from typing import Optional
from bson import ObjectId

class EventReferenceEmbedded(PydanticBaseModel):
    id: ObjectId = Field(..., alias="_id", description="Event ID")
    # TODO
    model_config = {
        "arbitrary_types_allowed": True,
        "populate_by_name": True
    }