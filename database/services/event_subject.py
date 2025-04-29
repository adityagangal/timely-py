from typing import List, Dict
from bson import ObjectId
import traceback
from .event import fetch_event_map
from .subject import fetch_subject_map
from ..utils import build_bulk_operations, perform_bulk_updates, make_ref
from ..models import Event, Subject
import asyncio
from pymongo import UpdateOne
from database.config import get_connection
from ..utils import bulk_push_oid_links, hydrate_references

make_event_ref, event_projection = make_ref("id") # , "start_time", "end_time", "online_links", "description", "faculties", "subjects", "rooms", "day_of_week")
make_subject_ref, subject_projection = make_ref("id", "name", "code")

# async def join_event_subject(event_subject_mapping: Dict[str, List[str]]):
#     try:
#         object_mapping: Dict[ObjectId, List[ObjectId]] = {
#             ObjectId(eid): [ObjectId(sid) for sid in sids]
#             for eid, sids in event_subject_mapping.items()
#         }

#         event_ids = list(object_mapping.keys())
#         subject_ids = list({sid for sids in object_mapping.values() for sid in sids})

#         event_map, subject_map = await asyncio.gather(
#             fetch_event_map(event_ids),
#             fetch_subject_map(subject_ids)
#         )

#         event_ops, subject_ops = build_bulk_operations(
#             source_to_targets=object_mapping,
#             source_map=event_map,
#             target_map=subject_map,
#             make_source_ref=make_event_ref,
#             make_target_ref=make_subject_ref,
#             source_field="subjects",
#             target_field="events"
#         )

#         await perform_bulk_updates(Event, Subject, event_ops, subject_ops)

#         print("Successfully performed bulk join operations.")

#     except Exception as e:
#         print(f"Bulk join failed: {e}")
#         traceback.print_exc()

# async def join_event_subject_server_side(event_subject_mapping: dict, batch_size: int = 1000):
#     """
#     Push subject<->event ObjectIds, then hydrate Event.subjects with {id, name, code}
#     """
#     subject_ops, event_ops = [], []
#     db = get_connection()
#     event_coll = db["Events"]
#     subjects_coll = db["Subjects"]


#     for event_id, sub_ids in event_subject_mapping.items():
#         for sid in sub_ids:
#             event_ops.append(
#                 UpdateOne(
#                     {"_id": ObjectId(event_id)},
#                     {"$addToSet": {"subjects": ObjectId(sid)}}
#                 )
#             )
#             subject_ops.append(
#                 UpdateOne(
#                     {"_id": ObjectId(sid)},
#                     {"$addToSet": {"events": ObjectId(event_id)}}
#                 )
#             )

#     # Bulk write operations
#     for ops, coll in ((subject_ops, subjects_coll), (event_ops, event_coll)):
#         for i in range(0, len(ops), batch_size):
#             batch = ops[i:i + batch_size]
#             if batch:
#                 await coll.bulk_write(batch)

#     # Hydrate Event.subjects
#     await event_coll.aggregate([
#         {"$lookup": {
#             "from": "Subjects",
#             "localField": "subjects",
#             "foreignField": "_id",
#             "as": "subject_docs"
#         }},
#         {"$set": {
#             "subjects": {
#                 "$map": {
#                     "input": "$subject_docs",
#                     "as": "s",
#                     "in": {
#                         "id": "$$s._id",
#                         "name": "$$s.name",
#                         "code": "$$s.code"
#                     }
#                 }
#             }
#         }},
#         {"$unset": "subject_docs"},
#         {"$merge": {
#             "into": "Events",
#             "on": "_id",
#             "whenMatched": "merge",
#             "whenNotMatched": "discard"
#         }}
#     ]).to_list(length=None)

async def join_event_subject_server_side(event_subject_mapping: dict, batch_size: int = 1000):
    try:
        db = get_connection()
        event_coll = db["Events"]
        subject_coll = db["Subjects"]

        await bulk_push_oid_links(
            mapping=event_subject_mapping,
            source_field="events",
            target_field="subjects",
            source_coll=subject_coll,
            target_coll=event_coll,
            batch_size=batch_size,
        )

        await hydrate_references(
            coll=event_coll,
            local_field="subjects",
            from_collection="Subjects",
            foreign_field="_id",
            out_field="subjects",
            projection_map={"id": "_id", "name": "name", "code": "code"},
        )
        print("Successfully performed bulk join operations.")
    except Exception as e:
        print(f"Bulk join failed: {e}")
        traceback.print_exc()
