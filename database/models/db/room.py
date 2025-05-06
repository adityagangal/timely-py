from ..core import BaseDocument
from pydantic import Field
from typing import List, Optional
from ..embedded import EventId

class Room(BaseDocument):
    code: str = Field(..., description="Room code")
    events: Optional[List[EventId]] = Field(default=[], description="Events associated with the Room")
    
    class Settings:
        name = "Rooms"

# TODO Can experiment here with keeping all events start and end times, for quick finding if Room is empty
# Can use EventIdStartEnd here
# Can add more room info here
# type
# description
# facilities