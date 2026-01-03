from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.schemas import Category, CategoryCreate, CategoryUpdate
from crud.crud import get_categories, get_category, create_category, update_category, delete_category
from db.session import get_db
from uuid import UUID

router = APIRouter()


@router.get("/", response_model=list[Category])
async def read_categories(user_id: UUID = Query(...), db: AsyncSession = Depends(get_db)):
    return await get_categories(db, user_id)


@router.post("/", response_model=Category)
async def create_new_category(category: CategoryCreate, user_id: UUID = Query(...), db: AsyncSession = Depends(get_db)):
    return await create_category(db, category, user_id)


@router.get("/{category_id}", response_model=Category)
async def read_category(category_id: UUID, user_id: UUID = Query(...), db: AsyncSession = Depends(get_db)):
    db_category = await get_category(db, category_id, user_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category


@router.put("/{category_id}", response_model=Category)
async def update_existing_category(category_id: UUID, category_update: CategoryUpdate, user_id: UUID = Query(...), db: AsyncSession = Depends(get_db)):
    db_category = await update_category(db, category_id, category_update, user_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category


@router.delete("/{category_id}")
async def delete_existing_category(category_id: UUID, user_id: UUID = Query(...), db: AsyncSession = Depends(get_db)):
    success = await delete_category(db, category_id, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category deleted"}