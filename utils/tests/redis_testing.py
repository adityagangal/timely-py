from database.services import find_user_events, explain_user_events
from database.dummy.redis_tests import get_events_for_user_fast, get_events_with_lua
from bson import ObjectId

async def test(user_ids: str):
    async def test_helper(user_id):
        _, m_time, l1 = await find_user_events(ObjectId(user_id))
        # await explain_user_events(ObjectId(user_id))
        _, _, p_time, l2 = await get_events_for_user_fast(user_id)
        _, _, l_time, l3 = await get_events_with_lua(user_id)
        return m_time, p_time, l_time, l1, l2, l3

    
    a, b, c = 0, 0, 0
    arr = []

    for user_id in user_ids:
        for i in range(10):
            a1, b1, c1, l1, l2, l3 = await test_helper(user_id)
            a += a1
            b += b1
            c += c1
            arr.append((user_id, a1, b1, c1, l1, l2, l3))
    
    n = len(user_ids)
    
    print(f"Mongo Time: {a:.6f}, average = {(a/n):.6f}")
    print(f"Redis - Python: {b:.6f}, average = {(b/n):.6f}")
    print(f"Redis - Lua: {c:.6f}, average = {(c/n):.6f}")
    return arr