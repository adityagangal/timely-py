from models import LiveEvent, LiveEventEntry
from datetime import date

async def add_live_event_entry(date: date, entry: LiveEventEntry):
    await LiveEvent.find_one({"date": date}).upsert(
        {
            "$push": {"live_events": entry}
        },
        on_insert=LiveEvent(date=date, live_events=[entry])
    )

