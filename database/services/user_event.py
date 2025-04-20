from typing import List, Dict
from bson import ObjectId
import traceback
from .user import fetch_user_map
from .event import fetch_event_map
from ..utils import build_bulk_operations, perform_bulk_updates, make_ref
from ..models import User, Event
import asyncio

make_user_ref, user_projection = make_ref("id", "name")
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
            target_field="faculties"
        )

        await perform_bulk_updates(User, Event, user_ops, event_ops)

        print("Successfully performed bulk join operations.")

    except Exception as e:
        print(f"Bulk join failed: {e}")
        traceback.print_exc()