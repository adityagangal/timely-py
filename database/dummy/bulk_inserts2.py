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
            in_batches=[]
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
            in_batches=[]
        )
        for _ in range(count)
    ]




def random_time_range():
    start_hour = random.randint(8, 16)
    end_hour = random.randint(start_hour + 1, min(start_hour + 3, 20))
    return time(start_hour), time(end_hour)


def format_time(t: time) -> str:
    return t.strftime("%H:%M")

async def bulk_inserts():
    print("Creating batches...")
    batches: list[Batch] = [
        Batch(
            id=ObjectId(),
            name=f"{faker.word().capitalize()} Batch",
            code=generate_code("BATCH"),
            description=faker.sentence(),
            participants=[],
            events=[]
        )
        for _ in range(BATCH_COUNT)
    ]
    batch_map = {batch.id: batch for batch in batches}
    batch_refs = [BatchIdNameCode(_id=b.id, name=b.name, code=b.code) for b in batches]

    print("Creating students in bulk...")
    all_students = []
    for i in range(0, TOTAL_STUDENTS, STUDENT_CHUNK):
        print(f"Inserting students {i+1} to {i+STUDENT_CHUNK}")
        students = generate_students_bulk(STUDENT_CHUNK, [])  # Assign batches below
        all_students.extend(students)

    print("Creating faculty in bulk...")
    all_faculty = []
    for i in range(0, TOTAL_FACULTY, FACULTY_CHUNK):
        print(f"Inserting faculty {i+1} to {i+FACULTY_CHUNK}")
        faculty = generate_faculty_bulk(FACULTY_CHUNK, [])  # Assign batches below
        all_faculty.extend(faculty)

    print("Assigning batches to users and embedding participants...")
    def assign_batches_embed(users: list[User], min_batches=1, max_batches=3):
        for user in users:
            assigned_batches = random.sample(batch_refs, k=random.randint(min_batches, max_batches))
            user.in_batches = assigned_batches

            user_embed = UserIdNameTags(_id=user.id, name=user.name, tags=[])
            for b in assigned_batches:
                batch_map[b.id].participants.append(user_embed)

    assign_batches_embed(all_students, min_batches=1, max_batches=2)
    assign_batches_embed(all_faculty, min_batches=1, max_batches=3)

    print("Fetching subjects and rooms...")
    subjects = await Subject.find_all().to_list()
    rooms = await Room.find_all().to_list()

    print("Creating recurring events in memory and embedding into batches and faculty...")
    all_events = []
    faculty_map = {f.id: f for f in all_faculty}

    for _ in range(TOTAL_EVENTS):
        selected_batches = random.sample(batches, k=random.randint(1, min(3, len(batches))))
        selected_faculties = random.sample(all_faculty, k=random.randint(1, min(2, len(all_faculty))))
        selected_subjects = random.sample(subjects, k=random.randint(0, min(2, len(subjects)))) if subjects else []
        selected_rooms = random.sample(rooms, k=random.randint(0, min(1, len(rooms)))) if rooms else []

        batch_refs_event = [BatchIdNameCode(_id=b.id, name=b.name, code=b.code) for b in selected_batches]
        faculty_refs = [FacultyIdNameCode(_id=f.id, name=f.name, code=f.code) for f in selected_faculties]
        subject_refs = [SubjectIdName(_id=s.id, name=s.name) for s in selected_subjects]
        room_refs = [RoomIdCode(_id=r.id, code=r.code) for r in selected_rooms]

        start_time, end_time = random_time_range()
        start_str = format_time(start_time)
        end_str = format_time(end_time)

        event = RecurringEvent(
            id=ObjectId(),
            start_time=start_str,
            end_time=end_str,
            day_of_week=random.randint(1, 7),
            online_links=[faker.url()],
            description=faker.sentence(),
            batches=batch_refs_event,
            faculties=faculty_refs,
            subjects=subject_refs,
            rooms=room_refs,
        )

        all_events.append(event)

        embedded_event = RecurringEventEmbedded(
            _id=event.id,
            start_time=start_str,
            end_time=end_str,
            day_of_week=event.day_of_week,
            online_links=event.online_links,
            description=event.description,
            faculties=event.faculties,
            subjects=event.subjects,
            rooms=event.rooms
        )

        for b in selected_batches:
            b.events.append(embedded_event)

        for f in selected_faculties:
            faculty_map[f.id].faculty_events.append(embedded_event)

    print("Bulk inserting everything...")
    await Batch.insert_many(batches)
    await Student.insert_many(all_students)
    await Faculty.insert_many(all_faculty)
    await RecurringEvent.insert_many(all_events)

    print("All done!")
