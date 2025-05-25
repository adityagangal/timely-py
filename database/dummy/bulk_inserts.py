import asyncio
import random
from faker import Faker
from database.config import connect_db
from database.models import Batch, Faculty, Student, Subject, Room
from datetime import time
from typing import List
import uuid
from bson import ObjectId
from database.models import (
    Batch, Faculty, Student, Event, RecurringEvent, RecurringEventEmbedded,
    BatchIdNameCode, FacultyIdNameCode, SubjectIdName, RoomIdCode,
    UserIdNameTags, User
)
from beanie import PydanticObjectId

faker = Faker()

# Constants
TOTAL_STUDENTS = 9500
TOTAL_FACULTY = 500
TOTAL_EVENTS = 10000
BATCH_COUNT = 200

STUDENT_CHUNK = 500
FACULTY_CHUNK = 100
EVENT_CHUNK = 500



def generate_code(prefix: str):
    return f"{prefix.upper()}-{uuid.uuid4().hex}"


def generate_students_bulk(count: int, batch_ids: List[BatchIdNameCode]) -> List[Student]:
    return [
        Student(
            name=faker.name(),
            email=faker.unique.email(),
            password="12345678",
            uid=generate_code("UID"),
            semester=random.randint(1, 8),
            division=random.choice(["A", "B", "C", "D", "E", "F"]),
            passout=random.randint(2025, 2028),
            in_batches=random.sample(batch_ids, k=random.randint(1, 2))
        )
        for _ in range(count)
    ]


def generate_faculty_bulk(count: int, batch_ids: List[BatchIdNameCode]) -> List[Faculty]:
    return [
        Faculty(
            id=ObjectId(),
            name=faker.name(),
            email=faker.unique.email(),
            password="12345678",
            code=generate_code("FAC"),
            default_room=None,
            in_batches=random.sample(batch_ids, k=random.randint(1, 3))
        )
        for _ in range(count)
    ]


async def create_dummy_batch() -> Batch:
    code = generate_code("BATCH")
    batch = Batch(
        id=ObjectId(),
        name=f"{faker.word().capitalize()} Batch",
        code=code,
        description=faker.sentence()
    )
    await batch.insert()
    return batch


def random_time_range():
    start_hour = random.randint(8, 16)
    end_hour = random.randint(start_hour + 1, min(start_hour + 3, 20))
    return time(start_hour), time(end_hour)


def format_time(t: time) -> str:
    return t.strftime("%H:%M")


async def create_many_dummy_recurring_events(num_events: int,
                                             batches: list[Batch],
                                             faculties: list[Faculty],
                                             subjects: list,
                                             rooms: list):

    events_to_insert = []
    batch_event_map: dict[PydanticObjectId, list[RecurringEventEmbedded]] = {}
    faculty_event_map: dict[PydanticObjectId, list[RecurringEventEmbedded]] = {}

    for _ in range(num_events):
        selected_batches = random.sample(batches, k=random.randint(1, min(3, len(batches))))
        selected_faculties = random.sample(faculties, k=random.randint(1, min(2, len(faculties))))
        selected_subjects = random.sample(subjects, k=random.randint(0, min(2, len(subjects)))) if subjects else []
        selected_rooms = random.sample(rooms, k=random.randint(0, min(1, len(rooms)))) if rooms else []

        batch_refs = [BatchIdNameCode(_id=b.id, name=b.name, code=b.code) for b in selected_batches]
        faculty_refs = [FacultyIdNameCode(_id=f.id, name=f.name, code=f.code) for f in selected_faculties]
        subject_refs = [SubjectIdName(_id=s.id, name=s.name) for s in selected_subjects]
        room_refs = [RoomIdCode(_id=r.id, code=r.code) for r in selected_rooms]

        start_time, end_time = random_time_range()

        revent = RecurringEvent(
            id=ObjectId(), 
            start_time=format_time(start_time),
            end_time=format_time(end_time),
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
    # TODO - DO this in BULK
    for event in events_to_insert:
        revent_embedded = RecurringEventEmbedded(
            _id=event.id,
            start_time=event.start_time,
            end_time=event.end_time,
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

    for batch_id, embeds in batch_event_map.items():
        await Batch.find(Batch.id == batch_id).update(
            {"$push": {"events": {"$each": embeds}}}
        )

    for faculty_id, embeds in faculty_event_map.items():
        await Faculty.find(Faculty.id == faculty_id).update(
            {"$push": {"faculty_events": {"$each": embeds}}}
        )

    return inserted_events

def assign_batches_to_users(users: list[User], batch_refs: list[BatchIdNameCode], min_batches=1, max_batches=3):
    """
    Assign random batches to each user and return a mapping for batch participants.
    """
    batch_participant_map: dict[PydanticObjectId, list[UserIdNameTags]] = {}

    for user in users:
        assigned_batches = random.sample(batch_refs, k=random.randint(min_batches, max_batches))
        user.in_batches = assigned_batches

        user_embed = UserIdNameTags(id=user.id, name=user.name, tags=[])

        for batch in assigned_batches:
            batch_participant_map.setdefault(batch.id, []).append(user_embed)

    return batch_participant_map


async def bulk_inserts():
    print("Creating batches...")
    batches = [await create_dummy_batch() for _ in range(BATCH_COUNT)]
    batch_refs = [BatchIdNameCode(_id=b.id, name=b.name, code=b.code) for b in batches]

    print("Creating students in bulk...")
    all_students = []
    for i in range(0, TOTAL_STUDENTS, STUDENT_CHUNK):
        print(f"Inserting students {i+1} to {i+STUDENT_CHUNK}")
        students = generate_students_bulk(STUDENT_CHUNK, [])  # Empty for now, will assign below
        all_students.extend(students)

    print("Creating faculty in bulk...")
    all_faculty = []
    for i in range(0, TOTAL_FACULTY, FACULTY_CHUNK):
        print(f"Inserting faculty {i+1} to {i+FACULTY_CHUNK}")
        faculty = generate_faculty_bulk(FACULTY_CHUNK, [])  # Empty for now, will assign below
        all_faculty.extend(faculty)

    print("Assigning batches to users...")
    student_participants = assign_batches_to_users(all_students, batch_refs, min_batches=1, max_batches=2)
    faculty_participants = assign_batches_to_users(all_faculty, batch_refs, min_batches=1, max_batches=3)

    # Merge both participant maps
    batch_participant_map = student_participants
    for batch_id, faculty_embeds in faculty_participants.items():
        batch_participant_map.setdefault(batch_id, []).extend(faculty_embeds)

    print("Inserting users into DB...")
    await Student.insert_many(all_students)
    await Faculty.insert_many(all_faculty)

    print("Adding participants to batches...")
    for batch_id, participants in batch_participant_map.items():
        await Batch.find(Batch.id == batch_id).update(
            {"$push": {"participants": {"$each": participants}}}
        )

    print("Fetching subjects and rooms...")
    subjects = await Subject.find_all().to_list()
    rooms = await Room.find_all().to_list()

    print("Creating recurring events in bulk...")
    for i in range(0, TOTAL_EVENTS, EVENT_CHUNK):
        print(f"Inserting events {i+1} to {i+EVENT_CHUNK}")
        await create_many_dummy_recurring_events(
            num_events=EVENT_CHUNK,
            batches=batches,
            faculties=all_faculty,
            subjects=subjects,
            rooms=rooms
        )

    print("All done!")

