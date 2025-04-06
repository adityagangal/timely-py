from database.models import Batch

async def migrate_batch_fields():
    print("Migrating User fields...")
    result = await Batch.get_motor_collection().update_many(
        {"batch_code": {"$exists": True}},
        {
            "$rename": {
                "batch_code": "code",
            }
        }
    )
    print(f"Matched: {result.matched_count}, Modified: {result.modified_count}")

