from .schemas import PromotionCreate, PromotionUpdate
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import Optional, List

COLLECTION_NAME = "promotion"

async def create_promotion(db: AsyncIOMotorDatabase, promotion: PromotionCreate) -> dict:
    data = promotion.dict()
    result = await db[COLLECTION_NAME].insert_one(data)
    new_doc = await db[COLLECTION_NAME].find_one({"id": result.inserted_id})
    new_doc["id"] = str(new_doc.pop("id"))
    return new_doc

async def list_promotions(db: AsyncIOMotorDatabase) -> List[dict]:
    items = []
    cursor = db[COLLECTION_NAME].find({})
    async for doc in cursor:
        doc["id"] = str(doc.pop("_id"))
        items.append(doc)
    return items

async def get_promotion(db: AsyncIOMotorDatabase, id: int) -> Optional[dict]:
    from bson import ObjectId
    doc = await db[COLLECTION_NAME].find_one({"id": id})
    if doc:
        doc["id"] = str(doc.pop("_id"))
    return doc

async def update_promotion(db: AsyncIOMotorDatabase, id: int, update: PromotionUpdate) -> Optional[dict]:
    values = {k: v for k, v in update.dict(exclude_unset=True).items()}
    result = await db[COLLECTION_NAME].find_one_and_update(
        {"id": id}, {"$set": values}, return_document=True
    )
    if result:
        result["id"] = str(result.pop("_id"))
    return result

async def delete_promotion(db: AsyncIOMotorDatabase, id: int) -> bool:
    result = await db[COLLECTION_NAME].delete_one({"id": id})
    return result.deleted_count == 1
