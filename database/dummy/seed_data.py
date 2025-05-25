import asyncio
from .factory import create_dummy_batch, create_dummy_student, create_dummy_faculty, create_dummy_event
from models import init_db  # your Beanie init function
from typing import List

async def seed_all():
    await init_db()  # Your MongoDB connection

    batches = [await create_dummy_batch() for _ in range(5)]

    # Convert for reference
    batch_refs = [dict(id=b.id, name=b.name, code=b.code) for b in batches]

    # Create users linked to batches
    students = [await create_dummy_student(batch_refs) for _ in range(20)]
    faculties = [await create_dummy_faculty(batch_refs) for _ in range(5)]

    # Create events
    for _ in range(10):
        await create_dummy_event(batches, faculties)

    print("Dummy data inserted successfully.")

if __name__ == "__main__":
    asyncio.run(seed_all())
