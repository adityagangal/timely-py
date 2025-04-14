from typing import List, Dict
from bson import ObjectId
import traceback
from .user import fetch_user_map
from .batch import fetch_batch_map
from ..utils import build_bulk_operations, perform_bulk_updates, make_ref
from ..models import User, Batch
import asyncio

make_user_ref = make_ref("id", "name")
make_batch_ref = make_ref("id", "name", "code")

async def join_user_batch_subscribers(user_batch_mapping: Dict[str, List[str]]):
    try:
        object_mapping: Dict[ObjectId, List[ObjectId]] = {
            ObjectId(uid): [ObjectId(bid) for bid in bids]
            for uid, bids in user_batch_mapping.items()
        }

        user_ids = list(object_mapping.keys())
        batch_ids = list({bid for bids in object_mapping.values() for bid in bids})

        user_map, batch_map = await asyncio.gather(
            fetch_user_map(user_ids),
            fetch_batch_map(batch_ids)
        )

        user_ops, batch_ops = build_bulk_operations(
            source_to_targets=object_mapping,
            source_map=user_map,
            target_map=batch_map,
            make_source_ref=make_user_ref,
            make_target_ref=make_batch_ref,
            source_field="in_batches",
            target_field="subscribers"
        )

        await perform_bulk_updates(User, Batch, user_ops, batch_ops)

        print("Successfully performed bulk join operations.")

    except Exception as e:
        print(f"Bulk join failed: {e}")
        traceback.print_exc()