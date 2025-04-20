from ..utils import create_one, create_many, P, find_all, fetch_entity_map
from database.models import Room
from typing import List, Optional, Type, Union, Dict
from bson import ObjectId
from beanie import Document


async def create_room(room_data: dict):
    return await create_one(Room, room_data)

async def create_rooms(rooms_list_data: List[dict]):
    return await create_many(Room, rooms_list_data)

async def find_all_rooms(projection_model: Optional[Type[P]] = None, write_to_file: bool = False) -> Optional[List[Union[Room, P]]]:
    return await find_all(Room, projection_model, write_to_file)

async def fetch_room_map(room_ids: List[ObjectId], projection_model: Optional[Type[P]] = None, with_children: bool = True) -> Dict[ObjectId, Union[P, Document]]:
    return await fetch_entity_map(room_ids, Room, projection_model, with_children)
