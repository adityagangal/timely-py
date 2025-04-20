from ..models import Subject
from ..utils import prepare_objects

subject_keys = [
    "name",
    "code",
    "events"
]

subjects = [
    ["Big Data Analytics", "BDA", []],
    ["Natural Language Processing", "NLP", []],
    ["Cloud Architecture", "CA", []],
]

def get_subject_objects():
    return prepare_objects(subject_keys, subjects)