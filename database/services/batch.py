from ..models import Batch
from typing import Type, Optional, List, Union, Dict
from database.utils import find_all, P
from ..utils import create_one, create_many
from beanie import Document
from ..models.reference_models import BatchReferenceIdNameCode as BatchProjection
from bson import ObjectId

async def create_batch(batch_data: dict) -> Optional[Document]:
    return await create_one(Batch, batch_data)

async def create_batches(batches_data: list[dict]) -> Optional[List[Document]]:
    return await create_many(Batch, batches_data)

async def find_all_batches(projection_model: Optional[Type[P]] = None, write_to_file: bool = False) -> Optional[List[Union[Batch, P]]]:
    return await find_all(Batch, projection_model, write_to_file)
    
async def add_user_to_batch(batch_user_map: dict):
    pass

async def fetch_batch_map(batch_ids: List[ObjectId]) -> Dict[ObjectId, BatchProjection]:
    cursor = Batch.find({"_id": {"$in": batch_ids}}, projection_model=BatchProjection)
    batches = [batch async for batch in cursor]
    return {batch.id: batch for batch in batches}
