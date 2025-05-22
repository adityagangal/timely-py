from database.utils import prepare_objects
from bson import ObjectId
from datetime import time

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
# TODO The time field has changed, so 
recurring_events = [
    [time(13, 30), time(15, 30), [], "BDA Class", [], [], [], [], 2],
    [time(13, 30), time(15, 30), [], "NLP Class", [], [], [], [], 2],
    [time(15, 30), time(17, 30), [], "CA Lab", [], [], [], [], 2],
]

def get_recurring_event_objects():
    return prepare_objects(recurring_events_keys, recurring_events)