import time
from bson import ObjectId
from ..models import Announcement

async def create_announcement(content, batch_oid, created_by, time_created):

    await Announcement.find_one(
        {"batch_id": batch_oid},  # Match condition
        sort=[("created_at", -1)]
    ).update(
        {
            "$push": {
                "announcements": {
                    "_id": ObjectId(),  # Generate a new ObjectId
                    "created_by": created_by,
                    "content": content,
                    "mentions": [],
                    "sent_at": time_created,
                    "edited_at": time_created,
                    "edit_history": []
                }
            }
        },
    )