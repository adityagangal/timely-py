# def live_events_from_events():
#     """
#         1) Date (D) => day (d)
#         2) Find Events scheduled for D, and recurring ones on d
#         3) Find Events with overrides set to D 
#             3.1) Find Overrides where start date set to D
#             3.2) Pick the event id given
#         4) Check the overrides where the event in d, but is shifted to another date. These event are rescheduled away.
#         5) Use Events and Optional Override times to fill LiveEvents for D
#     """

from datetime import datetime
from database.models import Event, RecurringEvent, LiveEventEntry, LiveEvent, Override

async def aggregate_live_events_for_day(date: datetime):
    weekday = date.isoweekday() # 1-7 (Monday-Sunday)
    date_only = date.date

    # --- Pipeline to get all valid Events & RecurringEvents with optional override ---
    events_pipeline = [
        {
            "$match": {
                "$or": [
                    {"start_date": date_only},  # Normal Events
                    {"day_of_week": weekday}    # RecurringEvents
                ]
            }
        },
        {
            "$lookup": {  # Join Overrides for this date
                "from": "Override",
                "let": { "event_id": "$_id" },
                "pipeline": [
                    { "$match": {
                        "$expr": {
                            "$and": [
                                { "$eq": ["$date", date_only] },
                                { "$eq": ["$event_id", "$$event_id"] }
                            ]
                        }
                    }}
                ],
                "as": "override_info"
            }
        },
        {
            "$unwind": { "path": "$override_info", "preserveNullAndEmptyArrays": True }
        },
        {
            "$addFields": {
                "final_start_time": {
                    "$ifNull": ["$override_info.current_entry.start_time", "$start_time"]
                },
                "final_end_time": {
                    "$ifNull": ["$override_info.current_entry.end_time", "$end_time"]
                },
                "final_status": {
                    "$ifNull": ["$override_info.status", "scheduled"]
                }
            }
        },
        {
            "$project": {
                "_id": 1,
                "final_start_time": 1,
                "final_end_time": 1,
                "online_links": 1,
                "description": 1,
                "batches": 1,
                "faculties": 1,
                "subjects": 1,
                "rooms": 1,
                "final_status": 1
            }
        }
    ]

    # --- Pipeline to get IDs of events rescheduled away from `date` ---
    rescheduled_away_pipeline = [
        {
            "$match": {
                "current_entry.original_date": date_only
            }
        },
        {
            "$project": {
                "event_id": 1
            }
        }
    ]

    # Run both aggregations
    event_entries = await Event.aggregate(events_pipeline).to_list(None)
    print(event_entries)
    recurring_entries = await RecurringEvent.aggregate(events_pipeline).to_list(None)
    print(recurring_entries)
    rescheduled_away = await Override.aggregate(rescheduled_away_pipeline).to_list(None)

    rescheduled_ids = {r['event_id'] for r in rescheduled_away}

    # Merge and filter on app side
    all_entries = [*event_entries, *recurring_entries]
    filtered_entries = [e for e in all_entries if e["_id"] not in rescheduled_ids]

    # Build LiveEventEntry list
    live_entries = []
    for e in filtered_entries:
        start_datetime = datetime.combine(date_only, e['final_start_time'])
        end_datetime = datetime.combine(date_only, e['final_end_time'])

        entry = LiveEventEntry(
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            online_links=e.get("online_links", []),
            description=e.get("description"),
            batches=e.get("batches", []),
            faculties=e.get("faculties", []),
            subjects=e.get("subjects", []),
            rooms=e.get("rooms", [])
        )
        live_entries.append(entry)

    # Upsert into LiveEvent collection
    await LiveEvent.find_one(LiveEvent.date == date_only).upsert(
        {"$set": {"live_events": live_entries}},
        on_insert=LiveEvent(date=date_only, live_events=live_entries),
    )
