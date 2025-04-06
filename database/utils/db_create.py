from typing import List, Type, Optional
from beanie import Document
import traceback

async def create_one(Model: Type[Document], data: dict) -> Optional[Document]:
    try:
        model = Model(**data)
        await model.insert()
        print(f"{Model.__name__} {getattr(model, 'id', 'N/A')} created successfully.")
        return model
    except Exception as e:
        print(f"Failed to create {Model.__name__}: {e}")
        traceback.print_exc()
        return None

async def create_many(Model: Type[Document], data_list: List[dict]) -> Optional[List[Document]]:
    models = [Model(**data) for data in data_list]
    created_models = []
    try:
        result = await Model.insert_many(models, ordered=False)
        created_model_ids = set(result.inserted_ids)  # Track successful IDs
        created_models = [model for model in models if model.id in created_model_ids]
        print(f"All valid {Model.__name__} records inserted successfully.")
    except Exception as e:
        print(f"Some {Model.__name__} records failed to insert: {e}")
        traceback.print_exc()
    return created_models

