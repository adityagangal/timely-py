from typing import List, Dict
from bson import ObjectId
import traceback
from .user import fetch_user_map
from .batch import fetch_batch_map
from ..utils import build_bulk_operations, perform_bulk_updates, make_ref
from ..models import User, Batch
import asyncio

# TODO 
# create a new function join user batch server side

make_user_ref, user_projection = make_ref("id", "name")
make_batch_ref, batch_projection = make_ref("id", "name", "code")

# async def join_user_batch_subscribers(user_batch_mapping: Dict[str, List[str]]):
#     try:
#         object_mapping: Dict[ObjectId, List[ObjectId]] = {
#             ObjectId(uid): [ObjectId(bid) for bid in bids]
#             for uid, bids in user_batch_mapping.items()
#         }

#         user_ids = list(object_mapping.keys())
#         batch_ids = list({bid for bids in object_mapping.values() for bid in bids})

#         user_map, batch_map = await asyncio.gather(
#             fetch_user_map(user_ids, user_projection),
#             fetch_batch_map(batch_ids, batch_projection)
#         )

#         user_ops, batch_ops = build_bulk_operations(
#             source_to_targets=object_mapping,
#             source_map=user_map,
#             target_map=batch_map,
#             make_source_ref=make_user_ref,
#             make_target_ref=make_batch_ref,
#             source_field="in_batches",
#             target_field="subscribers"
#         )

#         await perform_bulk_updates(User, Batch, user_ops, batch_ops)

#         print("Successfully performed bulk join operations.")

#     except Exception as e:
#         print(f"Bulk join failed: {e}")
#         traceback.print_exc()

from database.config import get_connection
from ..utils import bulk_push_oid_links, hydrate_references

async def join_user_batch_participants(user_batch_mapping: Dict[str, List[str]]):
    try:

        db = get_connection()
        user_coll = db["Users"]
        batch_coll = db["Batches"]

        await bulk_push_oid_links(
            mapping=user_batch_mapping,
            source_field="in_batches",
            target_field="participants",
            source_coll=user_coll,
            target_coll=batch_coll,
        )

        await hydrate_references(
            coll=user_coll,
            local_field="in_batches",
            from_collection="batch",  # MongoDB collection name (not model)
            foreign_field="_id",
            out_field="in_batches",
            projection_map= {"id":"_id", "name":"name", "code":"code"},
        )

        await hydrate_references(
            coll=batch_coll,
            local_field="participants",
            from_collection="user",
            foreign_field="_id",
            out_field="participants",
            projection_map={"id":"_id", "name":"name", "tags": {"$literal": []}},
        )

        print("Successfully performed bulk join operations.")
    except Exception as e:
        print(f"Bulk join failed: {e}")
        traceback.print_exc()