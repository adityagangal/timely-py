from pydantic import BaseModel, Field
from beanie import PydanticObjectId

class RoomIdCode(BaseModel):
    id: PydanticObjectId = Field(..., alias="_id", description="Room document _id")
    code: str = Field(..., description="Room Code")