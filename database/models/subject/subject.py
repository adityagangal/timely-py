from ..base_model import BaseModel
from pydantic import Field
from beanie import Indexed, Link
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..batch.batch import Batch
    from ..event.event import Event

class Subject(BaseModel):
    name: str = Field(..., description="Subject name")
    code: str = Field(..., description="Subject code")
    # batches: Optional[List[Link["Batch"]]] = Field(default=[], description="Batches associated with the subject")
    events: Optional[List[Link["Event"]]] = Field(default=[], description="Events associated with the subject")

    class Settings:
        name = "Subjects"

from ..batch.batch import Batch
from ..event.event import Event

Subject.model_rebuild()