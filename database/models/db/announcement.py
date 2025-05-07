from ..core import BaseDocument
from pydantic import Field
from typing import List
from beanie import PydanticObjectId
from ..embedded import InnerAnnouncementEntry
    
class Announcement(BaseDocument):
    batch_id: PydanticObjectId = Field(..., description="Batch ID")
    announcements: List[InnerAnnouncementEntry] = Field(default=[], description="Chunk of announcements")
    class Settings:
        name = "Announcements"
# Can extend Inner Announcement
# reactions: Optional[List[Reactions]]
# seen by: Optional