from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RescheduleEntry(BaseModel):
    start_datetime: datetime
    end_datetime: datetime
    reason: Optional[str] = None

# TODO Can add support for change in faculty, etc. 