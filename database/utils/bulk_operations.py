from typing import List, Dict, Tuple, Callable, Any
from pymongo import UpdateOne
from bson import ObjectId

def build_bulk_operations(
    source_to_targets: Dict[ObjectId, List[ObjectId]],
    source_map: Dict[ObjectId, Any],
    target_map: Dict[ObjectId, Any],
    make_source_ref: Callable[[Any], dict],
    make_target_ref: Callable[[Any], dict],
    source_field: str,
    target_field: str
) -> Tuple[List[UpdateOne], List[UpdateOne]]:

    source_updates: List[UpdateOne] = []
    target_updates: List[UpdateOne] = []

    for source_id, target_ids in source_to_targets.items():
        source = source_map.get(source_id)
        if not source:
            print(f"Source {source_id} not found.")
            continue

        source_ref = make_source_ref(source)

        for target_id in target_ids:
            target = target_map.get(target_id)
            if not target:
                print(f"Target {target_id} not found.")
                continue

            target_ref = make_target_ref(target)

            source_updates.append(UpdateOne(
                {"_id": source_ref["id"]},
                {"$addToSet": {source_field: target_ref}},
                upsert=False
            ))

            target_updates.append(UpdateOne(
                {"_id": target_ref["id"]},
                {"$addToSet": {target_field: source_ref}},
                upsert=False
            ))

    return source_updates, target_updates

async def perform_bulk_updates(
    source_model,
    target_model,
    source_ops: List[UpdateOne],
    target_ops: List[UpdateOne],
    chunk_size: int = 100
):
    def chunk_operations(ops: List[UpdateOne], size: int) -> List[List[UpdateOne]]:
        return [ops[i:i + size] for i in range(0, len(ops), size)]
    
    if source_ops:
        for chunk in chunk_operations(source_ops, chunk_size):
            await source_model.get_motor_collection().bulk_write(chunk, ordered=False)

    if target_ops:
        for chunk in chunk_operations(target_ops, chunk_size):
            await target_model.get_motor_collection().bulk_write(chunk, ordered=False)