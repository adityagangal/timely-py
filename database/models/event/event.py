from ..base_model import BaseModel
from pydantic import Field
from beanie import Indexed, Link
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..batch.batch import Batch
    from ..user.base_user import User

class Event(BaseModel):
    start_time: str = Field(..., description="Start time in hh:mm")
    end_time: str = Field(..., description="End time in hh:mm")
    location: str = Field(..., description="Location")
    online_link: Optional[str] = Field(None, description="Online Link")
    description: Optional[str] = Field(None, description="Describe the event")
    batches: Optional[List[Link["Batch"]]] = Field(default=[], description="Batches associated with the event")
    faculty: Optional[List[Link["User"]]] = Field(default=[], description="Faculty associated with the event")

    class Settings:
        name = "Events"

from ..batch.batch import Batch
from ..user.base_user import User

Event.model_rebuild()