import time
from bson import ObjectId
from ..models import Announcement

async def create_announcement(content, batch_oid, created_by, time_created):
    pipeline = [
        {
            "$match": { "batch_id" : batch_oid }
        },
        {
            "$sort": { "serial_no": -1 }
        },
        {
            "$limit": 1
        }, 
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
        }
    ]
    
    # await create_new_announcement_with_model(batch_id=batch_id)

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