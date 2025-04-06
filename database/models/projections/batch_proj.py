from pydantic import BaseModel, Field
from beanie import PydanticObjectId

class BatchIdCodeProjection(BaseModel):
    id: PydanticObjectId = Field(..., alias="_id")
    batch_code: str