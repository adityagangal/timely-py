from database.models import User

async def migrate_user_fields():
    print("Migrating User fields...")
    result = await User.get_motor_collection().update_many(
        {"faculty_code": {"$exists": True}},
        {
            "$rename": {
                "faculty_code": "code",
            }
        }
    )
    print(f"Matched: {result.matched_count}, Modified: {result.modified_count}")

