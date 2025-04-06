from .event import Event
from pydantic import Field

"""event_keys = [
    "start_time", 
    "end_time", 
    "location",
    "online_link",
    "description",
    "batches",
]"""

class RecurringEvent(Event):
    day_of_week: int = Field(..., description="Day of Week (1, 7)<==>(Sunday, Saturday)")
    class Settings:
        name = "Recurring Events"