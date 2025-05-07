from pydantic import Field, BaseModel
from typing import Optional, List
from datetime import datetime, timezone
from beanie import PydanticObjectId
from bson import ObjectId

class EditHistoryEntry(BaseModel):
    content: str = Field(..., description="Previous version of the announcement")
    edited_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class CreatedByEntry(BaseModel):
    id: PydanticObjectId = Field(..., description="id of creator", alias="_id")
    name: str = Field(..., description="Name of creator")

class InnerAnnouncementEntry(BaseModel):
    id: PydanticObjectId = Field(default_factory=ObjectId, alias="_id")
    created_by: CreatedByEntry = Field(..., description= "Announcement creator information")
    content: str = Field(..., description= "Content of the announcement")
    mentions: Optional[List[PydanticObjectId]] = Field(default=[], description= "OIDs of people mentioned")
    sent_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    edited_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    edit_history: Optional[List[EditHistoryEntry]] = Field(default=[], description="Edit history")