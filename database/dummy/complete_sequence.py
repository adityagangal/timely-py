from .users import get_student_objects, get_faculty_objects
from .batches import get_batch_objects
from .events import get_recurring_event_objects
from ..services import create_students, create_faculties, create_batches, create_recurring_events
from ..services import find_all_users, find_all_batches
from ..models.pydantic_models import UserIdNameProjection, BatchIdCodeProjection
from ..services import join_user_batch_participants, join_batch_event
from .user_to_batch import user_batch_mapping
from .batch_to_event import batch_event_mapping

# Do this sequence one step at a time. Update the BSON ids correctly

async def dummy_sequence():
    await create_students(get_student_objects())
    await create_faculties(get_faculty_objects())
    await create_batches(get_batch_objects())
    await find_all_users(UserIdNameProjection, True)
    await find_all_batches(BatchIdCodeProjection, True)
    await join_user_batch_participants(user_batch_mapping)
    await create_recurring_events(get_recurring_event_objects())
    await join_batch_event(batch_event_mapping)