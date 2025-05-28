from ..core import BaseDocument
from pydantic import Field
from typing import List
from beanie import PydanticObjectId
from ..embedded import InnerAnnouncementEntry
from bson import ObjectId
    
class Announcement(BaseDocument):
    batch_id: PydanticObjectId = Field(..., description="Batch ID")
    announcements: List[InnerAnnouncementEntry] = Field(default=[], description="Chunk of announcements")
    class Settings:
        name = "Announcements"
    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True
# Can extend Inner Announcement
# reactions: Optional[List[Reactions]]
# seen by: Optional