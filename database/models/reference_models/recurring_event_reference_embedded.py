from pydantic import BaseModel as PydanticBaseModel, Field
from typing import Optional, List
from bson import ObjectId
from .faculty_reference_id_name_code import FacultyReferenceIdNameCode
from .subject_reference_id_name import SubjectReferenceIdName
from .room_reference_id_code import RoomReferenceIdCode

class RecurringEventReferenceEmbedded(PydanticBaseModel):
    id: ObjectId = Field(..., alias="_id", description="Event ID")
    start_time: str = Field(..., description="Start time in hh:mm")
    end_time: str = Field(..., description="End time in hh:mm")
    online_links: Optional[List[str]] = Field(default=[], description="Online Links")
    description: Optional[str] = Field(None, description="Describe the event")
    faculties: Optional[List[FacultyReferenceIdNameCode]] = Field(default=[], description="Faculty associated with the event")
    subjects: Optional[List[SubjectReferenceIdName]] = Field(default=[], description="Subjects associated with the event")
    rooms: Optional[List[RoomReferenceIdCode]] = Field(default=[], description="Room Data")
    day_of_week: int = Field(..., description="Day of Week (1, 7)<==>(Sunday, Saturday)")
    
    model_config = {
        "arbitrary_types_allowed": True,
        "populate_by_name": True
    }