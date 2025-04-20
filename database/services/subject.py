from ..utils import create_one, create_many, P, find_all, fetch_entity_map
from database.models import Subject   
from typing import List, Optional, Type, Union, Dict
from bson import ObjectId
from beanie import Document

async def create_subject(subject_data: dict):
    return await create_one(Subject, subject_data)

async def create_subjects(subjects_list_data: List[dict]):
    return await create_many(Subject, subjects_list_data)

async def find_all_subjects(projection_model: Optional[Type[P]] = None, write_to_file: bool = False) -> Optional[List[Union[Subject, P]]]:
    return await find_all(Subject, projection_model, write_to_file)

async def fetch_subject_map(subject_ids: List[ObjectId], projection_model: Optional[Type[P]] = None, with_children: bool = True) -> Dict[ObjectId, Union[P, Document]]:
    return await fetch_entity_map(subject_ids, Subject, projection_model, with_children)
