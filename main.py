import asyncio
from database.config import connect_db, disconnect_db
from database.services import explain_user_events, find_user_events
from datetime import datetime, timezone
from database.models import CreatedByEntry

from typing import Dict, List
from bson import ObjectId
from pymongo import UpdateOne
from database.models import User, Event, RecurringEvent
from database.config import get_connection
from database.services.live_events_from_events import aggregate_live_events_for_day
from database.services.test import push_into_latest_hello, create_new_announcement_with_model
from database.services.announcement import create_announcement
from utils.logging_config import setup_logging
from database.dummy.bulk_inserts2 import bulk_inserts
from database.dummy.redis_tests import get_all_events_for_user, get_events_for_user_fast
import time

async def main():
    setup_logging()
    await connect_db()
    # print(*await find_user_events(ObjectId('6833741b5ca5db3e8e2bad95')), sep = "\n")
    # print()
    # print(*await find_user_events(ObjectId('683374355ca5db3e8e2d3436')), sep = "\n")
    # await explain_user_events(ObjectId('6833741b5ca5db3e8e2bad95'))
    # await explain_user_events(ObjectId('683374355ca5db3e8e2d3436'))
    # print(await User.aggregate([
    #         { "$match": { "_id": ObjectId("6833606987b738a31529a9d7") } },
    #         { "$unwind": "$in_batches" },
    #         {
    #             "$lookup": {
    #             "from": "Batches",
    #             "localField": "in_batches.id",
    #             "foreignField": "_id",
    #             "as": "matched"
    #             }
    #         }
    #     ]).to_list(None))
    # await create_new_announcement_with_model(ObjectId("67fbe9baa73a6a81e5e65b0f"))
    # await push_into_latest_hello(ObjectId("67fbe9baa73a6a81e5e65b0f"))
    # await create_announcement("This is an actual Announcement!!!", ObjectId("67fbe9baa73a6a81e5e65b0f"), CreatedByEntry(_id=ObjectId("67fbe790993d093f6b3a9480"), name="Rishi Tiku"), datetime.now(timezone.utc))
    # await aggregate_live_events_for_day(datetime(2025, 5, 21)) # Not working RN, because date is broken in old version.
    # await bulk_inserts()

    # d = datetime(2025, 5, 20)
    # print(d.isoweekday())

    # event_entries = await Event.find({"start_date": d}).to_list(None)
    # recurring_entries = await RecurringEvent.get_motor_collection().find({"day_of_week": 3}).to_list(None)
    # print(event_entries, recurring_entries)
    # start_time = time.perf_counter()
    # events = get_all_events_for_user("6834ac6604c10774fb7c68e5")
    await get_events_for_user_fast("6834b365de3f30be5a114c03")
    # print(events)
    # end_time = time.perf_counter()
    # elapsed = end_time - start_time
    # print(f"Retrieved {len(events)} events in {elapsed:.4f} seconds")
    await disconnect_db()


# Standard Python entry point
if __name__ == "__main__":
    asyncio.run(main())


""" 
TODO - Done List
- Join Events to Batches - Done!!!!
- Query Users to Events - Done!!!! - 1ms max per query - OMG fast
- Join Users to Events - Done!!!
- Join Events to Subjects and Rooms - Done!!!
- Query Users to Events (subscribed + faculty) - Done!!!!
- Use new join operations instead of Bulk operations - Remove Bulk operations first, then think of a way
- to refactor all functions - Done!! Need to test them out once
- Reorganize Models Folder - Done!! Need to change Dummy Data to suit fields
- Create Announcements - Done!! 
- Make Overrides, Announcements, LiveEvents as Upsert Functions -  done

TODO 
- Bulk Operations functions need to be cleaned, and new functions to be tested- TODO
- Can change the Link types to Oid and Embedded types to Union of Embedded type and Oid - Not Required for now

- Need to do change Detection now, whenever a field gets changed, change that field to the corresponding 
- fields as well.

- Add Logic to create a new announcement chunk document if it nears 15MB - Cron Job

- Create Batch-Admins Logic
- Find person whereabouts
- Find empty rooms
- Change Updated at field


- Create Mapping for Recurring Event + Override to Live Event


- Change Events
- Create Factory functions for All to generate data


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

