from beanie import PydanticObjectId
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RescheduleEntry(BaseModel):
    id: PydanticObjectId
    start_datetime: datetime
    end_datetime: datetime
    reason: Optional[str] = None

# TODO Can add support for change in faculty, etc. 