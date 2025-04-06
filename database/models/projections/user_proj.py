from pydantic import BaseModel, Field
from beanie import PydanticObjectId

class UserIdNameProjection(BaseModel):
    id: PydanticObjectId = Field(..., alias="_id")
    name: str