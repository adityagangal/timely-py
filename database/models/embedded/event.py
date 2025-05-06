from pydantic import BaseModel, Field
from typing import Optional, List
from beanie import PydanticObjectId
from .user import FacultyIdNameCode
from .subject import SubjectIdName
from .room import RoomIdCode
from datetime import time

class RecurringEventEmbedded(BaseModel):
    id: PydanticObjectId = Field(..., alias="_id", description="Event ID")
    start_time: str = Field(..., description="Start time in hh:mm")
    end_time: str = Field(..., description="End time in hh:mm")
    online_links: Optional[List[str]] = Field(default=[], description="Online Links")
    description: Optional[str] = Field(None, description="Describe the event")
    faculties: Optional[List[FacultyIdNameCode]] = Field(default=[], description="Faculty associated with the event")
    subjects: Optional[List[SubjectIdName]] = Field(default=[], description="Subjects associated with the event")
    rooms: Optional[List[RoomIdCode]] = Field(default=[], description="Room Data")
    day_of_week: int = Field(..., description="Day of Week (1, 7)<==>(Sunday, Saturday)")
    
class EventId(BaseModel):
    id: PydanticObjectId = Field(..., alias="_id", description="Event ID")

class EventIdStartEnd(BaseModel):
    id: PydanticObjectId = Field(..., alias="_id", description="Event ID")
    start_time: time = Field(..., description="Start time in hh:mm")
    end_time: time = Field(..., description="End time in hh:mm") 