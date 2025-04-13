from database.config import get_connection, transaction
from typing import List, Dict, Tuple
from pydantic import BaseModel, Field
from beanie import PydanticObjectId
from bson import ObjectId
from pymongo import UpdateOne
import traceback
from ..models.reference_models import BatchReferenceIdNameCode as BatchProjection, UserReferenceIdName as UserProjection

def get_collections():
    conn = get_connection()
    return conn["Users"], conn["Batches"]

async def fetch_user_map(
    user_ids: List[ObjectId],
    users_collection
) -> Dict[str, UserProjection]:
    cursor = users_collection.find(
        {"_id": {"$in": user_ids}},
        projection={"_id": 1, "name": 1}
    )
    users = [UserProjection(**doc) async for doc in cursor]
    return {str(user.id): user for user in users}

async def fetch_batch_map(
    batch_ids: List[ObjectId],
    batches_collection
) -> Dict[str, BatchProjection]:
    cursor = batches_collection.find(
        {"_id": {"$in": batch_ids}},
        projection={"_id": 1, "name": 1, "code": 1}
    )
    batches = [BatchProjection(**doc) async for doc in cursor]
    return {str(batch.id): batch for batch in batches}

def build_bulk_operations(
    user_batch_mapping: Dict[str, List[str]],
    user_map: Dict[str, UserProjection],
    batch_map: Dict[str, BatchProjection]
) -> Tuple[List[UpdateOne], List[UpdateOne]]:

    user_updates: List[UpdateOne] = []
    batch_updates: List[UpdateOne] = []

    for user_id, batch_ids in user_batch_mapping.items():
        user = user_map.get(user_id)
        if not user:
            print(f"User {user_id} not found.")
            continue

        user_ref = {"_id": user.id, "name": user.name}

        for batch_id in batch_ids:
            batch = batch_map.get(batch_id)
            if not batch:
                print(f"Batch {batch_id} not found.")
                continue

            batch_ref = {"_id": batch.id, "name": batch.name, "code": batch.code}

            user_updates.append(UpdateOne(
                {"_id": user.id},
                {"$addToSet": {"in_batches": batch_ref}}
            ))

            batch_updates.append(UpdateOne(
                {"_id": batch.id},
                {"$addToSet": {"subscribers": user_ref}}
            ))

    return user_updates, batch_updates

async def perform_bulk_updates(
    users_collection,
    batches_collection,
    user_ops: List[UpdateOne],
    batch_ops: List[UpdateOne]
):
    if user_ops:
        await users_collection.bulk_write(user_ops, ordered=False)
    if batch_ops:
        await batches_collection.bulk_write(batch_ops, ordered=False)

# ------------------- Main Entry -------------------

async def join_user_batch(user_batch_mapping: Dict[str, List[str]]):
    users_collection, batches_collection = get_collections()

    try:
        user_ids = [ObjectId(uid) for uid in user_batch_mapping]
        batch_ids = list({ObjectId(bid) for bids in user_batch_mapping.values() for bid in bids})

        user_map = await fetch_user_map(user_ids, users_collection)
        batch_map = await fetch_batch_map(batch_ids, batches_collection)

        user_ops, batch_ops = build_bulk_operations(user_batch_mapping, user_map, batch_map)

        await perform_bulk_updates(users_collection, batches_collection, user_ops, batch_ops)

        print("Successfully performed bulk join operations.")

    except Exception as e:
        print(f"Bulk join failed: {e}")
        traceback.print_exc()
