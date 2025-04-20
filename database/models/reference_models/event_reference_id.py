from pydantic import BaseModel as PydanticBaseModel, Field
from bson import ObjectId

class EventReferenceId(PydanticBaseModel):
    id: ObjectId = Field(..., alias="_id", description="Event ID")
    # start_time: str = Field(..., description="Start time in hh:mm")
    # end_time: str = Field(..., description="End time in hh:mm") 
    # Can experiment with there later TODO

    model_config = {
        "arbitrary_types_allowed": True,
        "populate_by_name": True
    }