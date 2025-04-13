from __future__ import annotations
from ..base_model import BaseModel
from beanie import Indexed, Link
from pydantic import Field
from typing import List, TYPE_CHECKING, Optional, Annotated
from ..reference_models import EventReferenceEmbedded, UserReferenceIdName


if TYPE_CHECKING:
    from ..user.base_user import User  # Imported only for type hints
    from ..event.event import Event
    from ..live_event.live_event import LiveEvent


class Batch(BaseModel):
    name: str = Field(None, description="Name of the batch")
    code: Annotated[str, Indexed(unique=True)]
    description: Optional[str] = Field(None, description="Description of the batch")
    subscribers: Optional[List[UserReferenceIdName]] = Field(default=[], description="Users who get event notifications")
    admins: Optional[List[UserReferenceIdName]] = Field(default=[], description="Users with admin privileges")
    events: Optional[List[EventReferenceEmbedded]] = Field(default=[], description="Related event extended references")
    live_events: List[Link[LiveEvent]] = Field(default=[], description="Related live event IDs") #TODO - Change this to some embedded reference later

    class Settings:
        name = "Batches"

from ..user.base_user import User
from ..event.event import Event
from ..live_event.live_event import LiveEvent

Batch.model_rebuild()
