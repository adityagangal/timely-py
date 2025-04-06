from database.config import get_connection, transaction
from typing import List
import traceback
from bson import ObjectId

async def join_user_batch(user_batch_mapping: dict[str, List[str]]):
    conn = get_connection()
    users_collection = conn["Users"]
    batches_collection = conn["Batches"]
    for user_id, batches in user_batch_mapping.items():
        user_object_id = ObjectId(user_id)
        for batch_id in batches:
            batch_object_id = ObjectId(batch_id)
            try:
                async with transaction() as session:
                    await users_collection.update_one(
                        {"_id": user_object_id},
                        {"$addToSet": {"in_batches": batch_object_id}},
                        session=session
                    )
                    await batches_collection.update_one(
                        {"_id": batch_object_id},
                        {"$addToSet": {"event_subscribers": user_object_id}},
                        session=session
                    )
                print(f"Successfully joined user {user_id} with batch {batch_id}")
            except Exception as e:
                print(f"Failed to join user {user_id} with batch {batch_id}: {e}")
                traceback.print_exc()
