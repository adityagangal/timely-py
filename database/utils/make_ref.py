from typing import Callable, Any

def make_ref(*fields: str) -> Callable[[Any], dict]:
    return lambda obj: {field: getattr(obj, field) for field in fields}

