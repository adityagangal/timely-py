from typing import List, Dict
from bson import ObjectId
import traceback
from .user import fetch_user_map
from .event import fetch_event_map
from ..utils import build_bulk_operations, perform_bulk_updates, make_ref, build_bulk_operations_one_sided, reverse_mapping
from ..models import User, Event
import asyncio

make_user_ref, user_projection = make_ref("id", "name", "code")
make_event_ref, event_projection = make_ref("id", "start_time", "end_time", "online_links", "description", "faculties", "subjects", "rooms", "day_of_week")

async def join_user_event_faculties(user_event_mapping: Dict[str, List[str]]):
    try:
        object_mapping: Dict[ObjectId, List[ObjectId]] = {
            ObjectId(uid): [ObjectId(bid) for bid in bids]
            for uid, bids in user_event_mapping.items()
        }

        user_ids = list(object_mapping.keys())
        event_ids = list({eid for eids in object_mapping.values() for eid in eids})

        user_map, event_map = await asyncio.gather(
            fetch_user_map(user_ids, user_projection),
            fetch_event_map(event_ids, event_projection)
        )

        user_ops, event_ops = build_bulk_operations(
            source_to_targets=object_mapping,
            source_map=user_map,
            target_map=event_map,
            make_source_ref=make_user_ref,
            make_target_ref=make_event_ref,
            source_field="faculty_events",
            target_field="faculties",
            source_is_linked=False,
            target_is_linked=False
        )

        await perform_bulk_updates(User, Event, user_ops, event_ops)

        print("Successfully performed bulk join operations.")

    except Exception as e:
        print(f"Bulk join failed: {e}")
        traceback.print_exc()


async def join_user_event(user_event_mapping: Dict[str, List[str]]):
    try:
        object_mapping: Dict[ObjectId, List[ObjectId]] = {
            ObjectId(uid): [ObjectId(bid) for bid in bids]
            for uid, bids in user_event_mapping.items()
        }
        user_ids = list(object_mapping.keys())
        event_ids = list({eid for eids in object_mapping.values() for eid in eids})

        user_map = await fetch_user_map(user_ids, user_projection)
        event_ops = build_bulk_operations_one_sided(
            source_to_targets=object_mapping,
            source_map=user_map,
            make_source_ref=make_user_ref,
            target_field="faculties",
            source_is_linked=False
        )
        await perform_bulk_updates(None, Event, [], event_ops)
        event_map = await fetch_event_map(event_ids, event_projection)
        user_ops = build_bulk_operations_one_sided(
            source_to_targets=reverse_mapping(object_mapping),
            source_map=event_map,
            make_source_ref=make_event_ref,
            target_field="faculty_events",
            source_is_linked=False
        )
        await perform_bulk_updates(User, None, user_ops, [])
    except Exception as e:
        print(f"Bulk join failed: {e}")
        traceback.print_exc()
    
from typing import Dict, List
from bson import ObjectId
from pymongo import UpdateOne
from database.models import User, Event
from database.config import get_connection

async def join_user_event_server_side(
    object_mapping: Dict[ObjectId, List[ObjectId]],
    batch_size: int = 1000,
) -> None:
    """
    Perform a two-phase server-side join using only MongoDB operations:

    Phase 1: Push raw OID links into Event.faculties and User.faculty_events.
    Phase 2: Hydrate those arrays into full reference objects via aggregation pipelines.

    :param object_mapping: map of user_id -> list of event_ids
    :param batch_size: number of ops per bulk_write
    """
    db = get_connection()
    coll_event = db["Events"]
    coll_user = db["Users"]

    # Phase 1: push raw OIDs
    event_ops: List[UpdateOne] = []
    user_ops: List[UpdateOne] = []
    for user_id, event_ids in object_mapping.items():
        for eid in event_ids:
            event_ops.append(
                UpdateOne(
                    {"_id": ObjectId(eid)},
                    {"$addToSet": {"faculties": ObjectId(user_id)}}
                )
            )
            user_ops.append(
                UpdateOne(
                    {"_id": ObjectId(user_id)},
                    {"$addToSet": {"faculty_events": ObjectId(eid)}}
                )
            )
    # Execute bulk writes in batches
    for ops, collection in ((event_ops, coll_event), (user_ops, coll_user)):
        for i in range(0, len(ops), batch_size):
            batch = ops[i : i + batch_size]
            if batch:
                await collection.bulk_write(batch)

    # Phase 2a: hydrate Event.faculties
    await coll_event.aggregate([
        {"$lookup": {
            "from": "Users",
            "localField": "faculties",
            "foreignField": "_id",
            "as": "faculty_docs"
        }},
        {"$set": {
            "faculties": {
                "$map": {
                    "input": "$faculty_docs",
                    "as": "u",
                    "in": {"id": "$$u._id", "name": "$$u.name", "code": "$$u.code"}
                }
            }
        }},
        {"$unset": "faculty_docs"},
        {"$merge": {
            "into": "Events",
            "on":   "_id",
            "whenMatched":   "merge",
            "whenNotMatched": "discard"
        }}
    ]).to_list(length=None)

    # Phase 2b: hydrate User.faculty_events
    await coll_user.aggregate([
        {"$lookup": {
            "from": "Events",
            "localField": "faculty_events",
            "foreignField": "_id",
            "as": "event_docs"
        }},
        {"$set": {
            "faculty_events": {
                "$map": {
                    "input": "$event_docs",
                    "as": "e",
                    "in": {
                        "id":           "$$e._id",
                        "start_time":   "$$e.start_time",
                        "end_time":     "$$e.end_time",
                        "online_links": "$$e.online_links",
                        "description":  "$$e.description",
                        "faculties":    "$$e.faculties",
                        "subjects":     "$$e.subjects",
                        "rooms":        "$$e.rooms",
                        "day_of_week":  "$$e.day_of_week"
                    }
                }
            }
        }},
        {"$unset": "event_docs"},
        {"$merge": {
            "into": "Users",
            "on":   "_id",
            "whenMatched":   "merge",
            "whenNotMatched": "discard"
        }}
    ]).to_list(length=None)