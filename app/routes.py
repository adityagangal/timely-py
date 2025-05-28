from fastapi import APIRouter
from database.config import connect_db
from database.services.query import find_json_serializable_user_events, find_user_events
from bson import ObjectId


router = APIRouter()

@router.get("/")
def read_root():
    return {"message": "Hello FastAPI"}

@router.get(
    "/users/{user_id}/events",
    summary="Get the next 7 days of events for a user"
)
async def weekly_events(
    user_id: str
):
    # return await find_json_serializable_user_events(ObjectId(user_id))
    return await find_user_events(ObjectId(user_id))