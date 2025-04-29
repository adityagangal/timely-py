from pymongo import UpdateOne
from typing import Dict, List
from bson import ObjectId


# TODO - Test these functions once

async def bulk_push_oid_links(
    mapping: Dict[ObjectId, List[ObjectId]],
    source_field: str,
    target_field: str,
    source_coll,
    target_coll,
    batch_size: int = 1000,
):
    source_ops, target_ops = [], []

    for src_id, tgt_ids in mapping.items():
        for tid in tgt_ids:
            source_ops.append(
                UpdateOne({"_id": ObjectId(tid)}, {"$addToSet": {source_field: ObjectId(tid)}})
            )
            target_ops.append(
                UpdateOne({"_id": ObjectId(src_id)}, {"$addToSet": {target_field: ObjectId(src_id)}})
            )

    for ops, coll in ((source_ops, source_coll), (target_ops, target_coll)):
        for i in range(0, len(ops), batch_size):
            batch = ops[i : i + batch_size]
            if batch:
                await coll.bulk_write(batch)


async def hydrate_references(
    coll,
    local_field: str,
    from_collection: str,
    foreign_field: str,
    out_field: str,
    projection_map: Dict[str, str],
):
    await coll.aggregate([
        {"$lookup": {
            "from": from_collection,
            "localField": local_field,
            "foreignField": foreign_field,
            "as": f"{out_field}_docs"
        }},
        {"$set": {
            out_field: {
                "$map": {
                    "input": f"${out_field}_docs",
                    "as": "doc",
                    "in": {key: f"$$doc.{val}" for key, val in projection_map.items()}
                }
            }
        }},
        {"$unset": f"{out_field}_docs"},
        {"$merge": {
            "into": coll.name,
            "on": "_id",
            "whenMatched": "merge",
            "whenNotMatched": "discard"
        }}
    ]).to_list(length=None)
