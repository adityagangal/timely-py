from pydantic import BaseModel as PydanticBaseModel, Field
from bson import ObjectId

class RoomReferenceIdCode(PydanticBaseModel):
    id: ObjectId = Field(..., alias="_id", description="Room document _id")
    code: str = Field(..., description="Room Code")

    model_config = {
        "arbitrary_types_allowed": True,
        "populate_by_name": True
    }