from bson import ObjectId
from models import Override, RescheduleEntry, EventStatusEnum
from datetime import date
from typing import Optional
import logging

async def add_override_entry(date: date, event_id: ObjectId, entry: Optional[RescheduleEntry], is_cancelled = False):
    insert_doc = Override(date=date, event_id=event_id, override_history=[])
    update_fields = {}
    update_fields["$set"] = {}
    
    if is_cancelled:
        insert_doc.status = EventStatusEnum.cancelled
        update_fields["$set"]["status"] = EventStatusEnum.cancelled
    elif not entry:
        logging.warn("Nothing passed to RescheduleEntry and neither is it cancelled.")
        return
    else:
        insert_doc.override_history = [entry]
        update_fields["$push"] = {"override_history": entry}
        update_fields["$set"]["current_entry"] = entry
    
    await Override.find_one(
        {"date": date, "event_id": event_id}
    ).upsert(
        update_fields,
        on_insert= insert_doc,
    )