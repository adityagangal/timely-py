from typing import List, Dict
from bson import ObjectId
import traceback
from .event import fetch_event_map
from .subject import fetch_subject_map
from ..utils import build_bulk_operations, perform_bulk_updates, make_ref
from ..models import Event, Subject
import asyncio

make_event_ref, event_projection = make_ref("id") # , "start_time", "end_time", "online_links", "description", "faculties", "subjects", "rooms", "day_of_week")
make_subject_ref, subject_projection = make_ref("id", "name", "code")

async def join_event_subject(event_subject_mapping: Dict[str, List[str]]):
    try:
        object_mapping: Dict[ObjectId, List[ObjectId]] = {
            ObjectId(eid): [ObjectId(sid) for sid in sids]
            for eid, sids in event_subject_mapping.items()
        }

        event_ids = list(object_mapping.keys())
        subject_ids = list({sid for sids in object_mapping.values() for sid in sids})

        event_map, subject_map = await asyncio.gather(
            fetch_event_map(event_ids),
            fetch_subject_map(subject_ids)
        )

        event_ops, subject_ops = build_bulk_operations(
            source_to_targets=object_mapping,
            source_map=event_map,
            target_map=subject_map,
            make_source_ref=make_event_ref,
            make_target_ref=make_subject_ref,
            source_field="subjects",
            target_field="events"
        )

        await perform_bulk_updates(Event, Subject, event_ops, subject_ops)

        print("Successfully performed bulk join operations.")

    except Exception as e:
        print(f"Bulk join failed: {e}")
        traceback.print_exc()