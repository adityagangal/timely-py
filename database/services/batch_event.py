from typing import List, Dict
from bson import ObjectId
import traceback
from .event import fetch_event_map
from .batch import fetch_batch_map
from ..utils import build_bulk_operations, perform_bulk_updates, make_ref
from ..models import Batch, Event
import asyncio

make_batch_ref, batch_projection = make_ref("id", "name", "code")
make_event_ref, event_projection = make_ref("id", "start_time", "end_time", "online_links", "description", "faculties", "subjects", "rooms", "day_of_week")

async def join_batch_event(batch_event_mapping: Dict[str, List[str]]):
    try:
        object_mapping: Dict[ObjectId, List[ObjectId]] = {
            ObjectId(uid): [ObjectId(bid) for bid in bids]
            for uid, bids in batch_event_mapping.items()
        }

        batch_ids = list(object_mapping.keys())
        event_ids = list({bid for bids in object_mapping.values() for bid in bids})

        batch_map, event_map = await asyncio.gather(
            fetch_batch_map(batch_ids, batch_projection),
            fetch_event_map(event_ids, event_projection),
        )

        batch_ops, event_ops = build_bulk_operations(
            source_to_targets=object_mapping,
            source_map=batch_map,
            target_map=event_map,
            make_source_ref=make_batch_ref,
            make_target_ref=make_event_ref,
            source_field="events",
            target_field="batches"
        )

        await perform_bulk_updates(Batch, Event, batch_ops, event_ops)

        print("Successfully performed bulk join operations.")

    except Exception as e:
        print(f"Bulk join failed: {e}")
        traceback.print_exc()


from typing import Dict, List
from bson import ObjectId
from pymongo import UpdateOne
from database.config import get_connection

async def join_batch_event_server_side(
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
    coll_batch = db["Batches"]

    # Phase 1: push raw OIDs
    event_ops: List[UpdateOne] = []
    batch_ops: List[UpdateOne] = []
    for batch_id, event_ids in object_mapping.items():
        for eid in event_ids:
            event_ops.append(
                UpdateOne(
                    {"_id": ObjectId(eid)},
                    {"$addToSet": {"batches": ObjectId(batch_id)}}
                )
            )
            batch_ops.append(
                UpdateOne(
                    {"_id": ObjectId(batch_id)},
                    {"$addToSet": {"events": ObjectId(eid)}}
                )
            )
    # Execute bulk writes in batches
    for ops, collection in ((event_ops, coll_event), (batch_ops, coll_batch)):
        for i in range(0, len(ops), batch_size):
            batch = ops[i : i + batch_size]
            if batch:
                await collection.bulk_write(batch)

    # Phase 2a: hydrate Event.batches
    await coll_event.aggregate([
        {"$lookup": {
            "from": "Batches",
            "localField": "batches",
            "foreignField": "_id",
            "as": "batch_docs"
        }},
        {"$set": {
            "batches": {
                "$map": {
                    "input": "$batch_docs",
                    "as": "b",
                    "in": {"id": "$$b._id", "name": "$$b.name", "code": "$$b.code"}
                }
            }
        }},
        {"$unset": "batch_docs"},
        {"$merge": {
            "into": "Events",
            "on":   "_id",
            "whenMatched":   "merge",
            "whenNotMatched": "discard"
        }}
    ]).to_list(length=None)

    # Phase 2b: hydrate Batch.events
    await coll_batch.aggregate([
        {"$lookup": {
            "from": "Events",
            "localField": "events",
            "foreignField": "_id",
            "as": "event_docs"
        }},
        {"$set": {
            "events": {
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
            "into": "Batches",
            "on":   "_id",
            "whenMatched":   "merge",
            "whenNotMatched": "discard"
        }}
    ]).to_list(length=None)