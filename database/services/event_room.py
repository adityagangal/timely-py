from typing import List, Dict
from bson import ObjectId
import traceback
from .event import fetch_event_map
from .room import fetch_room_map
from ..utils import build_bulk_operations, perform_bulk_updates, make_ref
from ..models import Event, Room
import asyncio

make_event_ref, event_projection = make_ref("id") # , "start_time", "end_time", "online_links", "description", "faculties", "rooms", "rooms", "day_of_week")
make_room_ref, room_projection = make_ref("id", "code")

async def join_event_room(event_room_mapping: Dict[str, List[str]]):
    try:
        object_mapping: Dict[ObjectId, List[ObjectId]] = {
            ObjectId(eid): [ObjectId(rid) for rid in rids]
            for eid, rids in event_room_mapping.items()
        }

        event_ids = list(object_mapping.keys())
        room_ids = list({rid for rids in object_mapping.values() for rid in rids})

        event_map, room_map = await asyncio.gather(
            fetch_event_map(event_ids),
            fetch_room_map(room_ids)
        )

        event_ops, room_ops = build_bulk_operations(
            source_to_targets=object_mapping,
            source_map=event_map,
            target_map=room_map,
            make_source_ref=make_event_ref,
            make_target_ref=make_room_ref,
            source_field="rooms",
            target_field="events"
        )

        await perform_bulk_updates(Event, Room, event_ops, room_ops)

        print("Successfully performed bulk join operations.")

    except Exception as e:
        print(f"Bulk join failed: {e}")
        traceback.print_exc()