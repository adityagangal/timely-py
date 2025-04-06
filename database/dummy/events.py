from database.utils import prepare_objects
from bson import ObjectId

event_keys = [
    "start_time", 
    "end_time", 
    "location",
    "online_link",
    "description",
    "batches",
    "subjects",
]

recurring_events_ukeys = ["day_of_week"]
recurring_events_keys = event_keys + recurring_events_ukeys

recurring_events = [
    ["13:30", "15:30", "409", None, "BDA Class", [ObjectId("67e259725489208758d2f3a4")], [], 3],
    ["13:30", "15:30", "407", None, "NLP Class", [ObjectId("67e259725489208758d2f3a3")], [], 3],
    ["15:30", "17:30", "406-A", None, "CA Lab", [ObjectId("67e259725489208758d2f3a5")], [], 3],
]

def get_recurring_event_objects():
    return prepare_objects(recurring_events_keys, recurring_events)