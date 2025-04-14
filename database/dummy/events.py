from database.utils import prepare_objects
from bson import ObjectId

event_keys = [
    "start_time", 
    "end_time",
    "online_links",
    "description",
    "batches",
    "faculties",
    "subjects",
    "rooms",

]

recurring_events_ukeys = ["day_of_week"]
recurring_events_keys = event_keys + recurring_events_ukeys

recurring_events = [
    ["13:30", "15:30", [], "BDA Class", [], [], [], [], 3],
    ["13:30", "15:30", [], "NLP Class", [], [], [], [], 3],
    ["15:30", "17:30", [], "CA Lab", [], [], [], [], 3],
]

def get_recurring_event_objects():
    return prepare_objects(recurring_events_keys, recurring_events)