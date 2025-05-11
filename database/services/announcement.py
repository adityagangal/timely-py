import time
from ..models import Announcement, InnerAnnouncementEntry

async def create_announcement(content, batch_oid, created_by, time_created, mentions = []):
    entry = InnerAnnouncementEntry(
        created_by = created_by,
        content = content,
        mentions = mentions,
        sent_at = time_created,
        edited_at = time_created,
        edit_history = []
    )
    await Announcement.find_one(
        {"batch_id": batch_oid},  # Match condition
        sort=[("created_at", -1)]
    ).upsert(
        {
            "$push": {
                "announcements": entry
            }
        },
        on_insert = Announcement(batch_id=batch_oid, announcements=[entry])
    )