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
        query = model.find_many({}, with_children=True)
        if projection_model is not None:
            results = await query.project(projection_model).to_list()
        else:
            raw_results = await query.to_list()
            results = []
            processed_ids = set()
            for item in raw_results:
                if str(item.id) in processed_ids:
                    continue
                processed_ids.add(str(item.id))
                if hasattr(item, "model_type") and item.model_type != model.__name__:
                    specific_class = find_class_by_name(item.model_type)
                    
                    if specific_class:
                        item_data = item.model_dump()
                        results.append(specific_class.model_validate(item_data))
                        continue
                results.append(item)
        
        if write_to_file:
            model_name = model.__name__
            proj_name = projection_model.__name__ if projection_model is not None else "Full"
            filename = f"{model_name}_{proj_name}.json"
            json_data = [item.model_dump() for item in results]
            await write_json_file(filename, json_data)
            print(f"Data written to {filename}")
        
        return results
    except Exception:
        traceback.print_exc()
        return None

def find_class_by_name(class_name: str) -> Optional[Type]:
    """Find a class by its name in the module's global namespace"""
    # This is a simplified approach - in production you might want to use a registry
    # to keep track of all model classes
    
    # Get the current module
    import sys
    current_module = sys.modules[__name__]
    
    # Try to find the class in the current module
    if hasattr(current_module, class_name):
        return getattr(current_module, class_name)
    
    # If not found, check all imported modules
    for module_name, module in sys.modules.items():
        if hasattr(module, class_name):
            return getattr(module, class_name)
    
    return None

