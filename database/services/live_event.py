from models import LiveEvent, LiveEventEntry
from datetime import date

async def add_live_event_entry(date: date, entry: LiveEventEntry):
    update_fields = {
        "$setOnInsert": {"date": date, "live_events": []},
        "$push": {"live_events": entry}
    }

    await LiveEvent.find_one({"date": date}).upsert(
        replacement=None,
        on_insert=update_fields["$setOnInsert"],
        on_update=update_fields
    )

