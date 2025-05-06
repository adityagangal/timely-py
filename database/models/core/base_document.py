from beanie import Document
from pydantic import Field
from datetime import datetime, timezone

class BaseDocument(Document):
    created_at: datetime = Field(default_factory= lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory= lambda: datetime.now(timezone.utc))

    class Settings:
        use_state_management = True
        validate_on_save = True
