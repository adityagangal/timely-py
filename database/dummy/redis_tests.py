import redis
import json
import time

r = redis.Redis(host="localhost", port=6379, decode_responses=True)



import asyncio
import time
import redis.asyncio as redis1

r1 = redis1.Redis(host="localhost", port=6379, decode_responses=True)

async def get_events_for_user_fast(user_id: str):
    start = time.perf_counter()

    user_key = f"user:{user_id}"
    user_data = await r1.json().get(user_key)
    
    if not user_data or "batch_ids" not in user_data:
        print(f"No batch_ids found for user {user_id}")
        return []

    batch_ids = user_data["batch_ids"]

    # Prepare tasks for concurrent fetching
    async def fetch_batch_events(batch_id):
        batch_key = f"batch:{batch_id}:events"
        return await r1.json().get(batch_key) or []

    tasks = [fetch_batch_events(batch_id) for batch_id in batch_ids]
    results = await asyncio.gather(*tasks)
    events = [event for batch_events in results for event in batch_events]
    end = time.perf_counter()

    # Flatten the list of lists into one list of events
    # print(f"Retrieved {len(events)} events for user {user_id} in {end - start:.4f} seconds")
    return events, results, end - start, len(events)


lua_script = """
local user_key = KEYS[1]
local batch_ids_json = redis.call("JSON.GET", user_key, ".batch_ids")
if not batch_ids_json then
    return cjson.encode({})
end
local batch_ids = cjson.decode(batch_ids_json)
local all_events = {}
for _, batch_id in ipairs(batch_ids) do
    local batch_key = "batch:" .. batch_id .. ":events"
    local events_json = redis.call("JSON.GET", batch_key, ".")
    if events_json then
        local events = cjson.decode(events_json)
        for _, event in ipairs(events) do
            table.insert(all_events, event)
        end
    end
end
return cjson.encode(all_events)
"""

async def get_events_with_lua(user_id: str):
    start = time.perf_counter()
    user_key = f"user:{user_id}"
    all_events_json = await r1.eval(lua_script, 1, user_key)
    end = time.perf_counter()
    # Decode returned JSON string into Python list
    import json
    events = json.loads(all_events_json)
    # print(f"Retrieved {len(events)} events for user {user_id} in {end - start:.4f} seconds")
    return events, all_events_json, end - start, len(events)