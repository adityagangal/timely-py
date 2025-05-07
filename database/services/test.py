from database.config import get_connection
from database.models import Announcement

async def push_into_latest_hello(batch_id, element=0):
    db = get_connection()
    coll = db["Announcements"]
    # await create_new_announcement_with_model(batch_id=batch_id)

    await coll.find_one_and_update(
        {"batch_id": batch_id},  # Match condition
        {
            "$push": {
                "announcements": "Hello world!1234" 
            }
        },
        sort=[("created_at", -1)]
    )


from beanie import PydanticObjectId
async def create_new_announcement_with_model(batch_id: PydanticObjectId):
    
    # Create a new Announcement object
    new_announcement = Announcement(
        batch_id=batch_id,
        announcements=[]  # Empty list initially
    )

    # Save to database
    await new_announcement.save()

    return new_announcement
