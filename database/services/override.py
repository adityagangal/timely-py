from bson import ObjectId
from models import Override, RescheduleEntry, EventStatusEnum
from datetime import date
from typing import Optional
import logging

async def add_override_entry(date: date, event_id: ObjectId, entry: Optional[RescheduleEntry], is_cancelled = False):
    update_fields = {
        "$setOnInsert": {"date": date, "event_id": event_id, "override_history": []},
    }
    if is_cancelled:
        update_fields["$set"] = {"status": EventStatusEnum.cancelled}
    elif not entry:
        logging.warn("Nothing passed to RescheduleEntry and neither is it cancelled.")
        return
    else:
        update_fields["$push"] = {"override_history": entry}
    await Override.find_one(
        {"date": date, "event_id": event_id}
    ).upsert(
        replacement=None,  # No replacement document, using update expression
        on_insert=update_fields["$setOnInsert"],
        on_update=update_fields
    )