import redis
import json
import time

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

def get_all_events_for_user(user_id: str):
    user_batches_key = f"user:{user_id}:batches"

    lua_script = """
    local batch_ids = redis.call('SMEMBERS', KEYS[1])
    local result = {}

    for _, batch_id in ipairs(batch_ids) do
        local events = redis.call('SMEMBERS', 'batch:' .. batch_id .. ':events')
        for _, event_json in ipairs(events) do
            table.insert(result, event_json)
        end
    end

    return result
    """

    start_time = time.time()
    raw_events = r.eval(lua_script, 1, user_batches_key)
    end_time = time.time()

    parsed_events = [json.loads(event) for event in raw_events]

    print(f"Retrieved {len(parsed_events)} events for user {user_id} in {end_time - start_time:.4f} seconds")
    return parsed_events

import asyncio
import time
import json
import redis.asyncio as redis1

r1 = redis1.Redis(host="localhost", port=6379, decode_responses=True)

async def get_events_for_user_fast(user_id: str):
    start = time.perf_counter()

    # 1. Get all batch_ids for the user (assuming still a set for batches)
    batch_ids = await r1.smembers(f"user:{user_id}:batches")

    # 2. For each batch_id, get the event documents from a Redis list
    events = []
    for batch_id in batch_ids:
        key = f"batch:{batch_id}:events"
        # Use LRANGE to get all events in the list
        raw_events = await r1.lrange(key, 0, -1)
        for ev in raw_events:
            try:
                events.append(json.loads(ev))
            except Exception:
                continue  # Skip bad JSON

    end = time.perf_counter()
    print(f"Retrieved {len(events)} events for user {user_id} in {end - start:.4f} seconds")
    return events
