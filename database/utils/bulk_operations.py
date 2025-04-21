from typing import List, Dict, Tuple, Callable, Any
from pymongo import UpdateOne
from bson import ObjectId

from pymongo import UpdateOne
from bson import ObjectId
from typing import Dict, List, Tuple, Callable, Any

from pymongo import UpdateOne
from bson import ObjectId
from typing import Dict, List, Tuple, Callable, Any

def build_bulk_operations(
    source_to_targets: Dict[ObjectId, List[ObjectId]],
    source_map: Dict[ObjectId, Any],
    target_map: Dict[ObjectId, Any],
    make_source_ref: Callable[[Any], dict],
    make_target_ref: Callable[[Any], dict],
    source_field: str,
    target_field: str,
    source_is_linked: bool = False,  # If source model uses linked references (e.g., ObjectId)
    target_is_linked: bool = False  # If target model uses linked references (e.g., ObjectId)
) -> Tuple[List[UpdateOne], List[UpdateOne]]:
    """
    Build bulk operations for adding references to List[Link[Model]] (linked) or List[EmbeddedModel] (embedded).

    Args:
        source_to_targets: Mapping from source ObjectId to a list of target ObjectIds.
        source_map: Source documents mapped by ObjectId.
        target_map: Target documents mapped by ObjectId.
        make_source_ref: Function to generate the source reference (ObjectId or embedded data).
        make_target_ref: Function to generate the target reference (ObjectId or embedded data).
        source_field: Field name in the source document to store the reference (e.g., "rooms").
        target_field: Field name in the target document to store the reference (e.g., "events").
        source_is_linked: Flag indicating if the source is a link reference (ObjectId).
        target_is_linked: Flag indicating if the target is a link reference (ObjectId).

    Returns:
        Tuple of (source updates, target updates) as lists of UpdateOne operations.
    """
    source_updates: List[UpdateOne] = []
    target_updates: List[UpdateOne] = []

    for source_id, target_ids in source_to_targets.items():
        source = source_map.get(source_id)
        if not source:
            print(f"Source {source_id} not found.")
            continue

        source_ref = make_source_ref(source) if not source_is_linked else {"id": source_id}

        for target_id in target_ids:
            target = target_map.get(target_id)
            if not target:
                print(f"Target {target_id} not found.")
                continue

            target_ref = make_target_ref(target) if not target_is_linked else {"id": target_id}

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


def build_bulk_operations_one_sided(
    source_to_targets: Dict[ObjectId, List[ObjectId]],
    source_map: Dict[ObjectId, Any],
    make_source_ref: Callable[[Any], dict],
    target_field: str,
    source_is_linked: bool = False,  # If source model uses linked references (e.g., ObjectId)
) -> Tuple[List[UpdateOne], List[UpdateOne]]:
    """
    Build bulk operations for adding references to List[Link[Model]] (linked) or List[EmbeddedModel] (embedded).

    Args:
        source_to_targets: Mapping from source ObjectId to a list of target ObjectIds.
        source_map: Source documents mapped by ObjectId.
        target_map: Target documents mapped by ObjectId.
        make_source_ref: Function to generate the source reference (ObjectId or embedded data).
        make_target_ref: Function to generate the target reference (ObjectId or embedded data).
        source_field: Field name in the source document to store the reference (e.g., "rooms").
        target_field: Field name in the target document to store the reference (e.g., "events").
        source_is_linked: Flag indicating if the source is a link reference (ObjectId).
        target_is_linked: Flag indicating if the target is a link reference (ObjectId).

    Returns:
        Tuple of (source updates, target updates) as lists of UpdateOne operations.
    """

    """
    Needs the ids to be validated beforehand.
    """
    target_updates: List[UpdateOne] = []

    for source_id, target_ids in source_to_targets.items():
        source = source_map.get(source_id)
        if not source:
            print(f"Source {source_id} not found.")
            continue

        source_ref = make_source_ref(source) if not source_is_linked else {"id": source_id}

        for target_id in target_ids:
            target_updates.append(UpdateOne(
                {"_id": target_id},
                {"$addToSet": {target_field: source_ref}},
                upsert=False
            ))

    return target_updates