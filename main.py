import asyncio
from database.config import connect_db, disconnect_db
from database.services import explain_user_events, find_user_events


from typing import Dict, List
from bson import ObjectId
from pymongo import UpdateOne
from database.models import User, Event
from database.config import get_connection

async def main():
    await connect_db()
    print(*await find_user_events(ObjectId("67fbe790993d093f6b3a9480")), sep = "\n")
    await disconnect_db()


# Standard Python entry point
if __name__ == "__main__":
    asyncio.run(main())


""" 
TODO
- Join Events to Batches - Done!!!!
- Query Users to Events - Done!!!! - 1ms max per query - OMG fast
- Join Users to Events - Done!!!
- Join Events to Subjects and Rooms - Done!!!
- Query Users to Events (subscribed + faculty) - Done!!!!
- Use new join operations instead of Bulk operations - Remove Bulk operations first, then think of a way
- to refactor all functions - Done!! Need to test them out once

TODO 
- Bulk Operations functions need to be cleaned, and new functions to be tested- TODO
- Can change the Link types to Oid and Embedded types to Union of Embedded type and Oid - Not Required for now

- Need to do change Detection now, whenever a field gets changed, change that field to the corresponding 
- fields as well.

- Create Announcements
- Create Batch-Admins Logic
- Find person whereabouts
- Find empty rooms
- Change Updated at field

- Reorganize models folder

""" 
















"""
    # await find_all_batches(BatchIdCodeProjection, write_to_file=True)
    # print(*get_student_objects(), sep="\n")
    # print(*get_faculty_objects(), sep="\n")
    # print(get_batch_objects())"migrate_user_fields",
    # await create_batches(get_batch_objects())
    # await migrate_batch_fields()
    # await create_students(get_student_objects())
    # await create_faculties(get_faculty_objects())
    # await find_all_users(UserIdNameProjection, write_to_file=True)
    # await create_batches(get_batch_objects())
    # await find_all_batches(write_to_file=True)
    # await join_user_batch_participants(user_batch_mapping)
    # await create_recurring_events(get_recurring_event_objects())
    # print(get_recurring_event_objects())
    # await migrate_add_subjects_field()
    # await migrate_user_fields()
    # await create_recurring_events(get_recurring_event_objects())
    # await find_all_events(write_to_file=True)
    # val = await ABC.find({}).to_list()
    # print(val)
    # await join_batch_event(batch_event_mapping)
    # print("Rishi")
    # print(*await find_user_events(ObjectId("67fbe790993d093f6b3a9480")), sep="\n")
    # print("Arsh")
    # print(*await find_user_events(ObjectId("67fbe790993d093f6b3a9481")), sep="\n")
    # print("Aparna")
    # print(*await find_user_events(ObjectId("67fbe7dbbf8ea406404f183b")), sep="\n")
    # print("Rishi")
    # await explain_user_events(ObjectId("67fbe790993d093f6b3a9480"))
    # print("Arsh")
    # await explain_user_events(ObjectId("67fbe790993d093f6b3a9481"))
    # print("Aparna")
    # await explain_user_events(ObjectId("67fbe7dbbf8ea406404f183b"))
    # await create_rooms(get_room_objects())
    # await create_subjects(get_subject_objects())
    # await find_all_rooms(write_to_file=True)
    # await find_all_subjects(write_to_file=True)
"""

