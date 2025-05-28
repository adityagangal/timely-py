import asyncio
from database.config import connect_db, disconnect_db
from database.services import explain_user_events, find_user_events
from datetime import datetime, timezone
from database.models import CreatedByEntry
import csv

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
from database.dummy.redis_tests import get_events_for_user_fast, get_events_with_lua
import time
import pprint
from utils.tests.redis_testing import test

async def main():
    setup_logging()
    await connect_db()
    # await find_user_events(ObjectId('68360a1bfd3232bea867b7dd'))
    # print()
    # print(*await find_user_events(ObjectId('6836037996d88cd9b9276545')), sep = "\n")
    # await explain_user_events(ObjectId('68360a1bfd3232bea867b7dd'))
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
    user_ids = [
    "68361215622b57e158498b80",
    "68361203622b57e158485ee2",
    "68361215622b57e1584991ed",
    "68361210622b57e158493a38",
    "68361200622b57e15848349f",
    "683611fb622b57e15847d4a2",
    "683611f6622b57e15847822d",
    "683611fc622b57e15847e54c",
    "6836120f622b57e158492c56",
    "683611fc622b57e15847ed1d",
    "6836120d622b57e158490af1",
    "6836120f622b57e158492bd2",
    "68361202622b57e158485d70",
    "68361200622b57e1584832ab",
    "683611fc622b57e15847e961",
    "683611f9622b57e15847ba35",
    "683611f7622b57e158479934",
    "68361200622b57e158482a26",
    "68361208622b57e15848bf76",
    "68361209622b57e15848cbaa",
    "68361205622b57e1584881a6",
    "6836120b622b57e15848ec88",
    "683611f9622b57e15847b8e5",
    "68361212622b57e1584959ef",
    "68361206622b57e158489b09",
    "683611f5622b57e158476a3d",
    "68361213622b57e158496593",
    "68361211622b57e158494c9b",
    "68361203622b57e158486c09",
    "6836120c622b57e15848fa01",
    "68361211622b57e158494494",
    "6836120c622b57e15848fc3a",
    "683611fb622b57e15847dbbf",
    "68361208622b57e15848bcdb",
    "6836120a622b57e15848dc00",
    "6836120d622b57e158491115",
    "68361201622b57e1584846fc",
    "683611fe622b57e158480926",
    "68361212622b57e158495849",
    "68361209622b57e15848c665",
    "683611fd622b57e15847f82b",
    "68361207622b57e15848af68",
    "683611f7622b57e158478b57",
    "683611f5622b57e15847661f",
    "68361208622b57e15848b629",
    "68361213622b57e15849734a",
    "68361209622b57e15848d407",
    "68361205622b57e1584888c0",
    "683611fd622b57e15847f61a",
    "683611fd622b57e15847f6b4",
    "683611f6622b57e158477dec",
    "6836120b622b57e15848f3a2",
    "683611fb622b57e15847decc",
    "68361214622b57e158497df9",
    "68361203622b57e158486a05",
    "68361209622b57e15848d421",
    "6836120b622b57e15848e83e",
    "6836120d622b57e158490937",
    "683611f8622b57e15847a3c4",
    "683611fd622b57e15847fbcd",
    "68361214622b57e1584978ab",
    "683611ff622b57e158481d88",
    "68361208622b57e15848bc54",
    "68361215622b57e158498dd9",
    "683611fd622b57e158480429",
    "683611fa622b57e15847c2ab",
    "683611f8622b57e15847aa97",
    "683611fd622b57e15847f967",
    "68361204622b57e15848776d",
    "683611f6622b57e158478707",
    "68361213622b57e158496b61",
    "683611f8622b57e158479a99",
    "68361205622b57e158488419",
    "68361200622b57e1584832d4",
    "6836120e622b57e1584918b4",
    "68361212622b57e158495eee",
    "68361214622b57e1584973d2",
    "6836120d622b57e158490d2c",
    "68361209622b57e15848d309",
    "683611f6622b57e1584776e9",
    "68361201622b57e158484827",
    "683611f6622b57e1584780e8",
    "68361210622b57e15849399f",
    "6836120d622b57e1584908b5",
    "68361201622b57e158484616",
    "683611fb622b57e15847e0c8",
    "68361208622b57e15848c3c0",
    "6836120a622b57e15848e091",
    "683611f9622b57e15847ad50",
    "683611f7622b57e15847886f",
    "6836120b622b57e15848eebf",
    "68361214622b57e158497b2a",
    "683611fa622b57e15847cad1",
    "68361205622b57e158488bd8",
    "6836120c622b57e15848f8cc",
    "683611f9622b57e15847baa9",
    "683611f5622b57e1584766b5",
    "68361214622b57e1584982d8",
    "68361203622b57e158486feb",
    "68361211622b57e158494a38"
]
    results = await test(user_ids)
    write_to_csv(results)


    # d = datetime(2025, 5, 20)
    # print(d.isoweekday())

    # event_entries = await Event.find({"start_date": d}).to_list(None)
    # recurring_entries = await RecurringEvent.get_motor_collection().find({"day_of_week": 3}).to_list(None)
    # print(event_entries, recurring_entries)
    # start_time = time.perf_counter()
    # events = get_all_events_for_user("6834ac6604c10774fb7c68e5")
    # events, res = await get_events_for_user_fast("68360a1bfd3232bea867b7dd")
    # await get_events_with_lua("68360a1bfd3232bea867b7dd")
    # print(events)
    # print(events == res)
    # pprint.pprint(res)
    # end_time = time.perf_counter()
    # elapsed = end_time - start_time
    # print(f"Retrieved {len(events)} events in {elapsed:.4f} seconds")
    await disconnect_db()

def write_to_csv(results):
    headers = ["user_id", "t1", "t2", "t3", "l1", "l2", "l3"]

# Write to CSV
    with open("results.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(headers)  # Write header row
        writer.writerows(results)  # Write data rows


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

