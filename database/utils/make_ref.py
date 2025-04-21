from pydantic import BaseModel, create_model, Field
from typing import Callable, Tuple, Type, Any, Optional
from bson import ObjectId

def make_ref(*fields: str) -> Tuple[Callable[[Any], dict], Type[BaseModel]]:
    field_definitions = {}

    for field in fields:
        if field == "id":
            field_definitions["id"] = (ObjectId, Field(..., alias="_id"))
        else:
            field_definitions[field] = (Optional[Any], ...)

    projection_model = create_model(
        "DynamicProjectionModel",
        __config__=type("Config", (), {"populate_by_name": True, "arbitrary_types_allowed": True}),
        **field_definitions,
    )

    def ref_func(doc: Any) -> dict:
        # This ensures we can extract values for embedding or linking
        return {
            key: getattr(doc, key)
            for key in fields
            if hasattr(doc, key)
        }

    return ref_func, projection_model


