from typing import Type, Optional, List, Dict, Union
from bson import ObjectId
from .types import T, P

async def fetch_entity_map(
    ids: List[ObjectId],
    model_class: T,
    projection_model: Optional[Type[P]] = None,
    with_children: bool = False
) -> Dict[ObjectId, Union[T, P]]:
    if not ids:
        return {}

    find_args = {"_id": {"$in": ids}}
    cursor = model_class.find(
        find_args,
        projection_model = projection_model,
        with_children = with_children
    )

    entities = [entity async for entity in cursor]
    return {entity.id: entity for entity in entities}
