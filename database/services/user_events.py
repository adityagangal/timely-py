from bson import ObjectId
from database.models import User
from beanie import PydanticObjectId

def get_pipeline(user_id: ObjectId):
    pipeline = [
        {"$match": {"_id": user_id}},
        {"$project": {"in_batches": 1 }},
        {"$lookup": {
            "from": "Batches",
            "localField": "in_batches.id",
            "foreignField": "_id",
            "as": "batch_docs"}
        },
        {"$unwind": "$batch_docs"},  # Unwind the batches, one per document
        {"$unwind": "$batch_docs.events"},  # Unwind the events inside each batch_doc
        {"$replaceRoot": {"newRoot": "$batch_docs.events"}},  # Replace root with each individual event
        {"$sort": { "day_of_week": 1, "start_time" : 1 }}
    ]
    return pipeline


async def find_user_events(user_id: ObjectId):
    pipeline = get_pipeline(user_id)
    return await User.aggregate(pipeline).to_list()

async def explain_user_events(user_id: PydanticObjectId) -> list[dict]:
    pipeline = get_pipeline(user_id)
    coll = User.get_motor_collection()
    db = coll.database
    explain_cmd = {
        "explain": {
            "aggregate": coll.name,
            "pipeline": pipeline,
            "cursor": {}
        },
        "verbosity": "executionStats"
    }
    stats = await db.command(explain_cmd)
    parsed = parse_explain_stats(stats)
    print_parsed_stats(parsed)
    return parsed


def parse_explain_stats(stats: dict) -> list[dict]:
    parsed = []
    for stage in stats.get("stages", []):
        stage_name = next((k for k in stage if k.startswith("$")), None)
        if not stage_name:
            continue
        entry = {"stage": stage_name}
        content = stage[stage_name]
        if isinstance(content, dict) and "executionStats" in content:
            es = content["executionStats"]
            entry.update({
                "nReturned": es.get("nReturned"),
                "totalDocsExamined": es.get("totalDocsExamined"),
                "time_ms": es.get("executionTimeMillis"),
            })
        else:
            entry.update({
                "nReturned": stage.get("nReturned"),
                "totalDocsExamined": stage.get("totalDocsExamined"),
                "time_ms": stage.get("executionTimeMillisEstimate"),
            })
        parsed.append(entry)
    return parsed


def print_parsed_stats(parsed: list[dict]):
    for p in parsed:
        stage   = p.get("stage", "")
        nret    = p.get("nReturned", "-")
        scanned = p.get("totalDocsExamined", "-")
        tms     = p.get("time_ms", "-")
        print(f"{stage:12} → returned={nret}, scanned={scanned}, time≈{tms} ms")

