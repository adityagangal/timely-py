from pydantic import BaseModel, create_model
from typing import Callable, Tuple, Type, Any

def make_ref(*fields: str) -> Tuple[Callable[[Any], dict], Type[BaseModel]]:
    def extractor(obj):
        return {field: getattr(obj, field) for field in fields}

    projection_model = create_model(
        'DynamicProjectionModel',
        **{field: (Any, ...) for field in fields}
    )

    return extractor, projection_model


