from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.schemas import User, UserCreate, UserUpdate
from crud.crud import get_user, get_user_by_email, create_user, update_user, delete_user
from db.session import get_db
from uuid import UUID

router = APIRouter()


@router.post("/", response_model=User)
async def create_new_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await create_user(db, user)


@router.get("/{user_id}", response_model=User)
async def read_user(user_id: UUID, db: AsyncSession = Depends(get_db)):
    db_user = await get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put("/{user_id}", response_model=User)
async def update_existing_user(user_id: UUID, user_update: UserUpdate, db: AsyncSession = Depends(get_db)):
    db_user = await update_user(db, user_id, user_update)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.delete("/{user_id}")
async def delete_existing_user(user_id: UUID, db: AsyncSession = Depends(get_db)):
    success = await delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}