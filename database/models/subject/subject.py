from ..base_model import BaseModel
from pydantic import Field
from beanie import Indexed, Link
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..batch.batch import Batch
    from ..event.event import Event

class Subject(BaseModel):
    subject_name: str = Field(..., description="Start time in hh:mm")
    subject_code: str = Field(..., description="End time in hh:mm")
    batches: Optional[List[Link["Batch"]]] = Field(default=[], description="Batches associated with the subject")
    events: Optional[List[Link["Event"]]] = Field(default=[], description="Events associated with the subject")

    class Settings:
        name = "Subjects"

from ..batch.batch import Batch
from ..event.event import Event

Subject.model_rebuild()