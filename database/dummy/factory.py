from faker import Faker
import random
import uuid
from datetime import time
from database.models import (Faculty, Student, Batch, Event,
                             BatchIdNameCode, FacultyIdNameCode, RecurringEvent,
                             RecurringEventEmbedded,
                             Subject, Room, SubjectIdName, RoomIdCode)

from typing import List
from beanie import PydanticObjectId

faker = Faker()

# Helper to generate a unique code
def generate_code(prefix: str):
    return f"{prefix.upper()}-{uuid.uuid4().hex[:6]}"

# Create a student
async def create_dummy_student(batch_ids: List[BatchIdNameCode]):
    student = Student(
        name=faker.name(),
        email=faker.unique.email(),
        password="dummyPass123",
        uid=generate_code("UID"),
        semester=random.randint(1, 8),
        division=random.choice(["A", "B", "C"]),
        passout=random.randint(2025, 2028),
        in_batches=batch_ids
    )
    await student.insert()
    return student

# Create a faculty
async def create_dummy_faculty(batch_ids: List[BatchIdNameCode]):
    faculty = Faculty(
        name=faker.name(),
        email=faker.unique.email(),
        password="dummyPass123",
        code=generate_code("FAC"),
        default_room=None,
        in_batches=batch_ids
    )
    await faculty.insert()
    return faculty

# Create a batch
async def create_dummy_batch():
    code = generate_code("BATCH")
    batch = Batch(
        name=f"{faker.word().capitalize()} Batch",
        code=code,
        description=faker.sentence(),
    )
    await batch.insert()
    return batch

# Create an event
async def create_dummy_event(batch_objs: List[Batch], faculty_objs: List[Faculty]):
    start_h = random.randint(9, 17)
    start_m = random.choice([0, 30])
    end = start_h + random.choice([1, 2])
    event = Event(
        start_time=time(hour=start_h, minute=start_m),
        end_time=time(hour=end, minute=start_m),
        online_links=[faker.url()],
        description=faker.sentence(),
        batches=[BatchIdNameCode(id=b.id, name=b.name, code=b.code) for b in batch_objs],
        faculties=[FacultyIdNameCode(id=f.id, name=f.name, code=f.code) for f in faculty_objs],
        subjects=[],  # You can build a similar factory for subjects
        rooms=[]
    )
    await event.insert()
    return event

def random_time_range():
    start_hour = random.randint(8, 16)
    end_hour = random.randint(start_hour + 1, min(start_hour + 3, 20))
    return time(start_hour), time(end_hour)

def format_time(t: time) -> str:
    return t.strftime("%H:%M")

async def create_many_dummy_recurring_events(num_events: int,
                                             batches: list[Batch],
                                             faculties: list[Faculty],
                                             subjects: list[Subject],
                                             rooms: list[Room]):

    events_to_insert = []
    batch_event_map: dict[PydanticObjectId, list[RecurringEventEmbedded]] = {}
    faculty_event_map: dict[PydanticObjectId, list[RecurringEventEmbedded]] = {}

    for _ in range(num_events):
        selected_batches = random.sample(batches, k=random.randint(1, min(3, len(batches))))
        selected_faculties = random.sample(faculties, k=random.randint(1, min(2, len(faculties))))
        selected_subjects = random.sample(subjects, k=random.randint(0, min(2, len(subjects)))) if subjects else []
        selected_rooms = random.sample(rooms, k=random.randint(0, min(1, len(rooms)))) if rooms else []

        batch_refs = [BatchIdNameCode(id=b.id, name=b.name, code=b.code) for b in selected_batches]
        faculty_refs = [FacultyIdNameCode(id=f.id, name=f.name, code=f.code) for f in selected_faculties]
        subject_refs = [SubjectIdName(id=s.id, name=s.name) for s in selected_subjects]
        room_refs = [RoomIdCode(id=r.id, code=r.code) for r in selected_rooms]

        start_time, end_time = random_time_range()

        revent = RecurringEvent(
            start_time=start_time,
            end_time=end_time,
            day_of_week=random.randint(1, 7),
            online_links=[faker.url()],
            description=faker.sentence(),
            batches=batch_refs,
            faculties=faculty_refs,
            subjects=subject_refs,
            rooms=room_refs,
        )

        events_to_insert.append(revent)

    inserted_events = await RecurringEvent.insert_many(events_to_insert)

    for event in inserted_events:
        revent_embedded = RecurringEventEmbedded(
            id=event.id,
            start_time=format_time(event.start_time),
            end_time=format_time(event.end_time),
            day_of_week=event.day_of_week,
            online_links=event.online_links,
            description=event.description,
            faculties=event.faculties,
            subjects=event.subjects,
            rooms=event.rooms
        )

        for b in event.batches:
            batch_event_map.setdefault(b.id, []).append(revent_embedded)

        for f in event.faculties:
            faculty_event_map.setdefault(f.id, []).append(revent_embedded)

    # BULK UPDATE BATCHES
    for batch_id, event_embeds in batch_event_map.items():
        await Batch.find(Batch.id == batch_id).update(
            {"$push": {"events": {"$each": event_embeds}}}
        )

    # BULK UPDATE FACULTIES
    for faculty_id, event_embeds in faculty_event_map.items():
        await Faculty.find(Faculty.id == faculty_id).update(
            {"$push": {"faculty_events": {"$each": event_embeds}}}
        )

    return inserted_events