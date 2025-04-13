from dummy import get_student_objects, get_faculty_objects, get_batch_objects
from ..services import create_students, create_faculties, create_batches
from ..services import find_all_users, find_all_batches
from ..models.projections import UserIdNameProjection, BatchIdCodeProjection

async def dummy_sequence():
    await create_students(get_student_objects())
    await create_faculties(get_faculty_objects())
    await create_batches(get_batch_objects())
    await find_all_users(UserIdNameProjection, True)
    await find_all_batches(BatchIdCodeProjection, True)