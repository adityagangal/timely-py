from beanie import PydanticObjectId
from bson import ObjectId
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from pydantic import Field, BaseModel
from ..embedded import BatchIdNameCode, FacultyIdNameCode, SubjectIdName, RoomIdCode

class LiveEventEmbedded(BaseModel):
    pass


class LiveEventEntry(BaseModel):
    id: PydanticObjectId = Field(default_factory=ObjectId)
    start_datetime: datetime = Field(..., description="Starting date and time")
    end_datetime: datetime = Field(..., description="Ending date and time")
    online_links: Optional[List[str]] = Field(default=[], description="Online Links")
    description: Optional[str] = Field(None, description="Describe the event")
    batches: Optional[List[BatchIdNameCode]] = Field(default=[], description="Batches associated with the event")
    faculties: Optional[List[FacultyIdNameCode]] = Field(default=[], description="Faculty associated with the event")
    subjects: Optional[List[SubjectIdName]] = Field(default=[], description="Subjects associated with the event")
    rooms: Optional[List[RoomIdCode]] = Field(default=[], description="Room Data")