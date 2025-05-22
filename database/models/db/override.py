from ..core import BaseDocument
from datetime import datetime
from pydantic import Field
from typing import Optional, List
from ..enums import EventStatusEnum
from beanie import PydanticObjectId
from ..embedded import RescheduleEntry

class Override(BaseDocument):
    date: datetime = Field(..., description="Source date of override")
    event_id: PydanticObjectId = Field(..., description="OId of Event")
    current_entry: RescheduleEntry = Field(..., description="Most recent Override Info")
    status: EventStatusEnum = Field(default=EventStatusEnum.rescheduled, description="Status of Live Event")
    override_history: Optional[List[RescheduleEntry]] = Field(default=[], description="History of Overrides")


