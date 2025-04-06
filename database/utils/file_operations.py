import os
import json
import aiofiles

async def write_json_file(filename: str, data: list) -> None:
    data_folder = "data"
    os.makedirs(data_folder, exist_ok=True)
    file_path = os.path.join(data_folder, filename)
    async with aiofiles.open(file_path, mode="w") as f:
        await f.write(json.dumps(data, indent=4, default=str))
