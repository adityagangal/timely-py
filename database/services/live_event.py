from models import LiveEvent, LiveEventEntry
from datetime import date

async def add_live_event_entry(date: date, entry: LiveEventEntry):
    await LiveEvent.get_motor_collection().update_one(
        {"date": date},
        {
            "$setOnInsert": {"date": date, "live_events": []},
            "$push": {"live_events": entry}
        },
        upsert=True
    )
