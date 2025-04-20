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