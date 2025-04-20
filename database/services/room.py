from ..utils import create_one, create_many, P, find_all
from database.models import Room
from typing import List, Optional, Type, Union

async def create_room(room_data: dict):
    return await create_one(Room, room_data)

async def create_rooms(rooms_list_data: List[dict]):
    return await create_many(Room, rooms_list_data)

async def find_all_rooms(projection_model: Optional[Type[P]] = None, write_to_file: bool = False) -> Optional[List[Union[Room, P]]]:
    return await find_all(Room, projection_model, write_to_file)