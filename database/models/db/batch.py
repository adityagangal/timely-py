from __future__ import annotations
from ..core import BaseDocument
from beanie import Indexed
from pydantic import Field
from typing import List, Optional, Annotated
from ..embedded import RecurringEventEmbedded, UserIdNameTags, LiveEventEmbedded

class Batch(BaseDocument):
    name: Optional[str] = Field(None, description="Name of the batch")
    code: Annotated[str, Indexed(unique=True)]
    description: Optional[str] = Field(None, description="Description of the batch")
    participants: Optional[List[UserIdNameTags]] = Field(default=[], description="Users with roles inside tags")
    events: Optional[List[RecurringEventEmbedded]] = Field(default=[], description="Related event embeds")
    live_events: Optional[List[LiveEventEmbedded]] = Field(default=[], description="Related live event embeds")

    class Settings:
        name = "Batches"


"""
Let's make 4 roles

- Subscriber - Gets all events, announcements
- Faculty - Similar to Admin, can write announcements, can add or remove users
- Admin - Can add or remove users
- Observer - Can open and see announcements and events, but doesn't get announcements and schedules

"""