import traceback
from typing import Type, TypeVar, List, Optional, Union
from pydantic import BaseModel
from beanie import Document
from .file_operations import write_json_file

T = TypeVar("T", bound=Document)
P = TypeVar("P", bound=BaseModel)

async def find_all(
    model: Type[T],
    projection_model: Optional[Type[P]] = None,
    write_to_file = False,
) -> Optional[List[Union[T, P]]]:
    try:
        query = model.find_many({})
        if projection_model is not None:
            query = query.project(projection_model)
        result = await query.to_list()
        if write_to_file:
            model_name = model.__name__
            proj_name = projection_model.__name__ if projection_model is not None else "Full"
            filename = f"{model_name}_{proj_name}.json"
            json_data = [item.model_dump() for item in result]
            await write_json_file(filename, json_data)
            print(f"Data written to {filename}")
        return result
    except Exception:
        traceback.print_exc()
        return None
