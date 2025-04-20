from database.utils import create_one, create_many, find_all, P
from database.models import RecurringEvent, Event
from typing import Optional, List, Dict, Type, Union
from beanie import Document
from bson import ObjectId
from ..utils import fetch_entity_map

async def create_recurring_event(recurring_event_data: dict) -> Optional[Document]:
    return await create_one(RecurringEvent, recurring_event_data)

async def create_recurring_events(recurring_events_data: list[dict]) -> Optional[List[Document]]:
    return await create_many(RecurringEvent, recurring_events_data)

async def fetch_event_map(event_ids: List[ObjectId], projection_model: Optional[Type[P]] = None, with_children: bool = True) -> Dict[ObjectId, Union[P, Document]]:
    return await fetch_entity_map(event_ids, Event, projection_model, with_children)

async def find_all_events(projection_model: Optional[Type[P]] = None, write_to_file: bool = False) -> Optional[List[Union[Event, P]]]:
    return await find_all(Event, projection_model, write_to_file)

async def find_all_recurring_events(projection_model: Optional[Type[P]] = None, write_to_file: bool = False) -> Optional[List[Union[RecurringEvent, P]]]:
    return await find_all(RecurringEvent, projection_model, write_to_file)