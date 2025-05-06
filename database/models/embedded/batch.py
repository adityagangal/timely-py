from pydantic import BaseModel, Field
from typing import Optional
from beanie import PydanticObjectId

class BatchIdCode(BaseModel):
    id: PydanticObjectId = Field(..., description="Batch Id", alias="_id")
    code: str = Field(..., description="Batch Code")

class BatchIdNameCode(BaseModel):
    id: PydanticObjectId = Field(..., alias="_id", description="Batch ID")
    name: Optional[str] = Field(..., description="Batch name")
    code: str = Field(default="", description="Batch code")