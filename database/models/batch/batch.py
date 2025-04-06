from __future__ import annotations
from ..base_model import BaseModel
from beanie import Indexed, Link
from pydantic import Field
from typing import List, TYPE_CHECKING
from typing import Annotated


if TYPE_CHECKING:
    from ..user.base_user import User  # Imported only for type hints
    from ..event.event import Event
    from ..live_event.live_event import LiveEvent


class Batch(BaseModel):
    batch_name: str = Field(None, description="Name of the batch")
    batch_code: Annotated[str, Indexed(unique=True)]
    description: str = Field(None, description="Description of the batch")
    event_subscribers: List[Link["User"]] = Field(default=[], description="Users who get event notifications")
    admins: List[Link["User"]] = Field(default=[], description="Users with admin privileges")
    events: List[Link["Event"]] = Field(default=[], description="Related event IDs")
    live_events: List[Link[LiveEvent]] = Field(default=[], description="Related live event IDs")

    class Settings:
        name = "Batches"

from ..user.base_user import User
from ..event.event import Event
from ..live_event.live_event import LiveEvent

Batch.model_rebuild()
