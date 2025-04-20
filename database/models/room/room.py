from ..base_model import BaseModel
from pydantic import Field
from beanie import Indexed, Link
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..event.event import Event

class Room(BaseModel):
    code: str = Field(..., description="Room code")
    events: Optional[List[Link["Event"]]] = Field(default=[], description="Events associated with the Room")
    # type
    # description
    # facilities
    class Settings:
        name = "Rooms"

from ..event.event import Event

Room.model_rebuild()