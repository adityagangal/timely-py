from database.models import Event

async def migrate_add_subjects_field():
    print("Running migration: Adding 'subjects' field to all Event documents...")
    result = await Event.get_motor_collection().update_many(
        {"subjects": {"$exists": False}},
        {"$set": {"subjects": []}}
    )
    print(f"Migration complete! Matched: {result.matched_count}, Modified: {result.modified_count}")


