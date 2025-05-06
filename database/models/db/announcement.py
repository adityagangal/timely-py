from ..core import BaseDocument
from pydantic import Field
from typing import Optional, List
from beanie import PydanticObjectId
from ..embedded import InnerAnnouncementEntry
    
class Announcement(BaseDocument):
    batch_id: PydanticObjectId = Field(..., description="Batch ID")
    announcements: Optional[List[InnerAnnouncementEntry]] = Field(default=[], description="List of all announcements")

# Can extend Inner Announcement
# reactions: Optional[List[Reactions]]
# seen by: Optional