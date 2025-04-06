from database.utils import create_one, create_many
from database.models import RecurringEvent
from typing import Optional, List
from beanie import Document

async def create_recurring_event(recurring_event_data: dict) -> Optional[Document]:
    return await create_one(RecurringEvent, recurring_event_data)

async def create_recurring_events(recurring_events_data: list[dict]) -> Optional[List[Document]]:
    return await create_many(RecurringEvent, recurring_events_data)