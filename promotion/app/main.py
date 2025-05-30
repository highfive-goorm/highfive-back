from fastapi import FastAPI, HTTPException, status, Depends
from typing import List
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import os

from .schemas import PromotionInDB, PromotionCreate, PromotionUpdate
from .crud import (
    create_promotion,
    get_promotion,
    list_promotions,
    update_promotion,
    delete_promotion,
)

app = FastAPI()

# MongoDB 연결 설정
MONGO_DETAILS = os.getenv("MONGO_DETAILS", "mongodb://localhost:27017")
client: AsyncIOMotorClient = AsyncIOMotorClient(MONGO_DETAILS)
db: AsyncIOMotorDatabase = client.get_database("mydatabase")  # 원하는 DB 이름

# Dependency 주입
async def get_db() -> AsyncIOMotorDatabase:
    return db

@app.post("/promotion", response_model=PromotionInDB, status_code=status.HTTP_201_CREATED)
async def create(promotion: PromotionCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    doc = await create_promotion(db, promotion)
    return PromotionInDB(**doc)

@app.get("/promotion", response_model=List[PromotionInDB])
async def list_all(db: AsyncIOMotorDatabase = Depends(get_db)):
    docs = await list_promotions(db)
    return [PromotionInDB(**doc) for doc in docs]

@app.get("/promotion/{id}", response_model=PromotionInDB)
async def get(id: int, db: AsyncIOMotorDatabase = Depends(get_db)):
    doc = await get_promotion(db, id)
    if not doc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Promotion not found")
    return PromotionInDB(**doc)

@app.put("/promotion/{id}", response_model=PromotionInDB)
async def update(id: int, update: PromotionUpdate, db: AsyncIOMotorDatabase = Depends(get_db)):
    doc = await update_promotion(db, id, update)
    if not doc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Promotion not found")
    return PromotionInDB(**doc)

@app.delete("/promotion/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: int, db: AsyncIOMotorDatabase = Depends(get_db)):
    deleted = await delete_promotion(db, id)
    if not deleted:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Promotion not found")
    return
