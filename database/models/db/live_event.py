from ..core import BaseDocument
from typing import List, Optional
from datetime import date as Date
from pydantic import Field
from ..embedded import LiveEventEntry
    

class LiveEvent(BaseDocument):
    date: Date = Field(..., description="Date for Live Events")
    live_events: Optional[List[LiveEventEntry]] = Field(default=[], description="Live Events for the day")
    class Settings:
        name = "LiveEvents"


# Think of logic where the event must be chopped up into different events
# because it covers two or more dates, because the date where it starts would be displayed,
# but not on the next day

# TODO - Split live events into multiple events - One per day